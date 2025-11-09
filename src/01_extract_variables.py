"""
MIMIC-IV Clinical Variable Extraction Pipeline
==============================================

Extract clinical variables (labs, vitals, GCS scores) from MIMIC-IV database
within the first 24 hours of ICU admission for refeeding syndrome study.

Author: James Green (jg1984@shp.rutgers.edu)
Created: 2024-10-17
Updated: 2025-11-06 (Documentation and cleanup for public release)

Description:
-----------
This script processes large MIMIC-IV CSV files in chunks to extract relevant
clinical measurements for a defined cohort of ICU patients. It filters data
to the first 24 hours of ICU stay and saves individual variable files for
downstream merging.

Input Files:
-----------
- cohort_definition.xlsx: Excel file defining the study cohort
  Required columns: subject_id, hadm_id, stay_id
- icustays.csv: MIMIC-IV ICU stay information
- labevents.csv: Laboratory measurements
- chartevents.csv: Vital signs and clinical assessments

Output Files:
------------
Feather files for each variable in temp_merge_files/:
- lab_platelet.feather
- lab_bilirubin.feather
- lab_creatinine.feather
- lab_pao2.feather
- chart_gcs_motor.feather
- chart_gcs_verbal.feather
- chart_gcs_eye.feather
- chart_temperature.feather
- chart_map.feather
- chart_fio2.feather

Usage:
------
    python 01_extract_variables.py

Configuration:
-------------
Update the BASE_PATH variable below to point to your MIMIC-IV data directory.
"""

import pandas as pd
import numpy as np
import os
from typing import Dict, Union, List, Tuple

# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_PATH = '/path/to/mimic-iv/'  # UPDATE THIS PATH
TEMP_PATH = os.path.join(BASE_PATH, 'temp_merge_files')
COHORT_FILE = '31May 2025 Scrubbing.xlsx'  # UPDATE FILENAME AS NEEDED
CHUNK_SIZE = 100000  # Number of rows to process at once

# Create output directory
os.makedirs(TEMP_PATH, exist_ok=True)

# =============================================================================
# MIMIC-IV ITEMID MAPPINGS
# =============================================================================

# Laboratory test item IDs
LAB_ITEMS = {
    'platelet': 51265,      # Platelet count (×10³/μL)
    'bilirubin': 50885,     # Total bilirubin (mg/dL)
    'creatinine': 50912,    # Creatinine (mg/dL)
    'pao2': 50821          # Partial pressure of oxygen (mmHg)
}

# Chart event item IDs
CHART_ITEMS = {
    'gcs_motor': 223901,    # Glasgow Coma Scale - Motor response
    'gcs_verbal': 223900,   # Glasgow Coma Scale - Verbal response
    'gcs_eye': 220739,      # Glasgow Coma Scale - Eye opening
    'temperature': 223761,  # Temperature (Celsius)
    'map': 220052,         # Mean arterial pressure (mmHg)
    'fio2': [223835, 3420] # Fraction of inspired oxygen (%)
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def load_cohort_data() -> Tuple[pd.DataFrame, Dict, set]:
    """
    Load and process cohort definition data.
    
    Returns:
    -------
    scrub : pd.DataFrame
        Cohort definition with subject_id, hadm_id, stay_id
    scrub_lookup : dict
        Dictionary mapping subject_id to list of stay records
    stay_ids : set
        Set of valid stay_ids in cohort
    """
    print("Loading cohort definition...")
    
    # Load cohort file
    scrub = pd.read_excel(
        os.path.join(BASE_PATH, COHORT_FILE),
        sheet_name='Data File',
        dtype=str
    )
    
    # Clean ID columns
    id_cols = ['subject_id', 'hadm_id', 'stay_id']
    scrub[id_cols] = scrub[id_cols].apply(lambda x: x.str.strip())
    scrub['stay_id'] = scrub['stay_id'].astype(str)
    
    stay_ids = set(scrub['stay_id'])
    
    # Load ICU stays to get admission times
    icustays = pd.read_csv(
        os.path.join(BASE_PATH, 'icustays.csv'),
        dtype=str
    )
    icustays['stay_id'] = icustays['stay_id'].astype(str)
    icustays = icustays[icustays['stay_id'].isin(stay_ids)].copy()
    icustays['intime'] = pd.to_datetime(icustays['intime'])
    
    # Map admission times to cohort
    scrub['intime'] = scrub['stay_id'].map(
        lambda sid: icustays.set_index('stay_id').loc[sid, 'intime']
    )
    
    # Create lookup dictionary for fast access
    scrub_lookup = (
        scrub.groupby('subject_id')[['stay_id', 'intime']]
        .apply(lambda g: g.to_dict('records'))
        .to_dict()
    )
    
    print(f"✅ Loaded {len(stay_ids)} ICU stays for {len(scrub_lookup)} patients")
    
    return scrub, scrub_lookup, stay_ids


def find_stay_for_measurement(row: pd.Series, 
                              scrub_lookup: Dict,
                              time_col: str) -> Union[Tuple[str, pd.Timestamp], None]:
    """
    Find the ICU stay that corresponds to a measurement time.
    
    Measurements are included if they occur within 24 hours of ICU admission.
    
    Parameters:
    ----------
    row : pd.Series
        Row containing subject_id and measurement time
    scrub_lookup : dict
        Lookup dictionary mapping subject_id to stay records
    time_col : str
        Name of column containing measurement timestamp
    
    Returns:
    -------
    tuple or None
        (stay_id, intime) if measurement falls within a valid stay window,
        None otherwise
    """
    subject_id = row['subject_id']
    measurement_time = row[time_col]
    
    # Check each ICU stay for this patient
    for stay_record in scrub_lookup.get(subject_id, []):
        intime = pd.to_datetime(stay_record['intime'])
        
        # Check if measurement is within 24 hours of admission
        if intime <= measurement_time <= intime + pd.Timedelta(hours=24):
            return stay_record['stay_id'], intime
    
    return None


def stream_aggregate_csv(file_path: str,
                         item_map: Dict,
                         time_col: str,
                         scrub: pd.DataFrame,
                         scrub_lookup: Dict,
                         stay_ids: set) -> Dict[str, pd.DataFrame]:
    """
    Stream process a large CSV file and aggregate measurements by stay_id.
    
    This function processes files in chunks to handle large MIMIC-IV tables
    without loading everything into memory.
    
    Parameters:
    ----------
    file_path : str
        Path to MIMIC-IV CSV file
    item_map : dict
        Mapping of variable names to itemid(s)
    time_col : str
        Name of timestamp column
    scrub : pd.DataFrame
        Cohort definition
    scrub_lookup : dict
        Fast lookup for subject-to-stay mapping
    stay_ids : set
        Valid stay_ids in cohort
    
    Returns:
    -------
    dict
        Dictionary mapping variable names to DataFrames containing
        stay_id, value, and timestamp
    """
    results = {}
    
    print(f"Processing {os.path.basename(file_path)} in chunks...")
    
    for chunk_num, chunk in enumerate(pd.read_csv(file_path, 
                                                   dtype=str,
                                                   chunksize=CHUNK_SIZE), 1):
        # Convert data types
        chunk['itemid'] = pd.to_numeric(chunk['itemid'], errors='coerce')
        chunk['valuenum'] = pd.to_numeric(chunk['valuenum'], errors='coerce')
        chunk[time_col] = pd.to_datetime(chunk[time_col], errors='coerce')
        
        # Filter to cohort subjects
        chunk = chunk[chunk['subject_id'].isin(scrub['subject_id'])].copy()
        
        if chunk.empty:
            continue
        
        # Find which ICU stay each measurement belongs to
        stay_info = chunk.apply(
            lambda row: find_stay_for_measurement(row, scrub_lookup, time_col),
            axis=1
        )
        
        # Filter to valid stays
        stay_info_filtered = stay_info[
            stay_info.apply(lambda x: isinstance(x, tuple) and len(x) == 2)
        ]
        
        if len(stay_info_filtered) == 0:
            continue
        
        # Create stay_id and intime columns
        valid_values = [x for x in stay_info_filtered if isinstance(x, tuple)]
        stay_info_df = pd.DataFrame(
            valid_values,
            columns=['stay_id', 'intime'],
            index=stay_info_filtered.index[:len(valid_values)]
        )
        
        # Join stay info to chunk
        chunk = chunk.loc[stay_info_df.index]
        chunk = chunk.drop(columns=['stay_id'], errors='ignore').join(stay_info_df)
        chunk = chunk[chunk['stay_id'].isin(stay_ids)]
        
        # Extract each variable
        for var_name, itemid in item_map.items():
            # Handle single itemid or list of itemids
            if isinstance(itemid, list):
                var_data = chunk[chunk['itemid'].isin(itemid)]
            else:
                var_data = chunk[chunk['itemid'] == itemid]
            
            # Select relevant columns
            var_data = (
                var_data[['stay_id', 'valuenum', time_col]]
                .dropna()
                .rename(columns={
                    'valuenum': var_name,
                    time_col: f'{var_name}_time'
                })
            )
            
            # Accumulate results
            if var_name not in results:
                results[var_name] = var_data
            else:
                results[var_name] = pd.concat([results[var_name], var_data])
        
        if chunk_num % 10 == 0:
            print(f"  Processed {chunk_num * CHUNK_SIZE:,} rows...")
    
    return results


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """
    Main execution function.
    """
    print("=" * 70)
    print("MIMIC-IV Variable Extraction for Refeeding Syndrome Study")
    print("=" * 70)
    
    # Load cohort data
    scrub, scrub_lookup, stay_ids = load_cohort_data()
    
    # Process laboratory events
    print("\n" + "=" * 70)
    print("EXTRACTING LABORATORY VALUES")
    print("=" * 70)
    
    lab_results = stream_aggregate_csv(
        file_path=os.path.join(BASE_PATH, 'labevents.csv'),
        item_map=LAB_ITEMS,
        time_col='charttime',
        scrub=scrub,
        scrub_lookup=scrub_lookup,
        stay_ids=stay_ids
    )
    
    # Save laboratory results
    for var_name, df in lab_results.items():
        output_path = os.path.join(TEMP_PATH, f'lab_{var_name}.feather')
        df.reset_index(drop=True).to_feather(output_path)
        print(f"✅ Saved: lab_{var_name}.feather ({len(df):,} measurements)")
    
    # Process chart events
    print("\n" + "=" * 70)
    print("EXTRACTING CHART EVENTS (VITALS & ASSESSMENTS)")
    print("=" * 70)
    
    chart_results = stream_aggregate_csv(
        file_path=os.path.join(BASE_PATH, 'chartevents.csv'),
        item_map=CHART_ITEMS,
        time_col='charttime',
        scrub=scrub,
        scrub_lookup=scrub_lookup,
        stay_ids=stay_ids
    )
    
    # Save chart results
    for var_name, df in chart_results.items():
        output_path = os.path.join(TEMP_PATH, f'chart_{var_name}.feather')
        df.reset_index(drop=True).to_feather(output_path)
        print(f"✅ Saved: chart_{var_name}.feather ({len(df):,} measurements)")
    
    print("\n" + "=" * 70)
    print("EXTRACTION COMPLETE")
    print("=" * 70)
    print(f"Output directory: {TEMP_PATH}")
    print("\nNext step: Run 02_merge_datasets.py to combine variables")


if __name__ == '__main__':
    main()
