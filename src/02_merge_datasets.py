"""
MIMIC-IV Dataset Merging Pipeline
==================================

Merge extracted clinical variables into a single analytical dataset.

Author: James Green (jg1984@shp.rutgers.edu)
Created: 2024-10-17
Updated: 2025-11-06 (Documentation and cleanup for public release)

Description:
-----------
This script merges individual variable files created by 01_extract_variables.py
into a single comprehensive dataset. Merging is performed in chunks to handle
large datasets efficiently.

Input Files:
-----------
- cohort_definition.xlsx: Cohort definition
- temp_merge_files/*.feather: Individual variable files

Output Files:
------------
- progressive_merge.csv: Combined dataset with all variables

Usage:
------
    python 02_merge_datasets.py

Configuration:
-------------
Update the BASE_PATH variable to match your data directory.
"""

import pandas as pd
import os
from typing import Dict

# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_PATH = '/path/to/mimic-iv/'  # UPDATE THIS PATH
TEMP_DIR = os.path.join(BASE_PATH, 'temp_merge_files')
COHORT_FILE = '31May 2025 Scrubbing.xlsx'  # UPDATE FILENAME AS NEEDED
OUTPUT_CSV = os.path.join(TEMP_DIR, 'progressive_merge.csv')
CHUNK_SIZE = 100000

# =============================================================================
# VARIABLE MAPPING
# =============================================================================

# Maps feather file names to standardized column names
VARIABLE_RENAME_MAP = {
    'lab_creatinine.feather': 'creatinine',
    'lab_bilirubin.feather': 'bilirubin',
    'lab_platelet.feather': 'platelet',
    'lab_pao2.feather': 'pao2',
    'chart_fio2.feather': 'fio2',
    'chart_temperature.feather': 'temperature',
    'chart_gcs_eye.feather': 'gcs_eye',
    'chart_gcs_motor.feather': 'gcs_motor',
    'chart_gcs_verbal.feather': 'gcs_verbal',
    'vaso_scores.feather': 'sofa_cardio'  # If vasopressor data available
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def initialize_base_file() -> None:
    """
    Create initial CSV with cohort stay_ids.
    
    This establishes the base dataset that will be progressively merged with
    each variable file.
    """
    print("Initializing base file with cohort...")
    
    # Load cohort definition
    scrub_df = pd.read_excel(
        os.path.join(BASE_PATH, COHORT_FILE),
        sheet_name='Data File',
        dtype=str
    )
    
    # Extract unique stays
    base = scrub_df[['subject_id', 'hadm_id', 'stay_id']].drop_duplicates()
    
    # Clean ID columns
    for col in ['subject_id', 'hadm_id', 'stay_id']:
        base[col] = (
            base[col]
            .astype(str)
            .str.strip()
            .str.replace('.0', '', regex=False)
        )
    
    # Save initial file
    base.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ Initialized base file → {OUTPUT_CSV}")
    print(f"   {len(base):,} unique ICU stays")


def merge_in_chunks(base_csv_path: str,
                   df_to_merge: pd.DataFrame,
                   key: str = 'stay_id') -> None:
    """
    Merge a DataFrame into an existing CSV file using chunked processing.
    
    This approach allows merging large files without loading everything into
    memory at once.
    
    Parameters:
    ----------
    base_csv_path : str
        Path to base CSV file
    df_to_merge : pd.DataFrame
        DataFrame to merge into base
    key : str
        Column name to merge on (default: 'stay_id')
    """
    temp_out = base_csv_path + '.tmp'
    
    reader = pd.read_csv(base_csv_path, dtype=str, chunksize=CHUNK_SIZE)
    
    with open(temp_out, 'w') as f_out:
        for i, chunk in enumerate(reader):
            # Merge this chunk
            merged = chunk.merge(df_to_merge, on=key, how='left')
            
            # Write with header only on first chunk
            merged.to_csv(f_out, index=False, mode='a', header=(i == 0))
    
    # Replace original with merged version
    os.replace(temp_out, base_csv_path)


def clean_id_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize ID column formats.
    
    Parameters:
    ----------
    df : pd.DataFrame
        DataFrame with ID columns
    
    Returns:
    -------
    pd.DataFrame
        DataFrame with cleaned ID columns
    """
    for id_col in ['subject_id', 'hadm_id', 'stay_id']:
        if id_col in df.columns:
            df[id_col] = (
                df[id_col]
                .astype(str)
                .str.strip()
                .str.replace('.0', '', regex=False)
            )
    return df


def process_variable_file(feather_file: str, 
                         new_col_name: str) -> pd.DataFrame:
    """
    Load and prepare a variable file for merging.
    
    Parameters:
    ----------
    feather_file : str
        Name of feather file
    new_col_name : str
        Standardized name for the variable column
    
    Returns:
    -------
    pd.DataFrame
        Prepared DataFrame with stay_id and variable columns
    """
    file_path = os.path.join(TEMP_DIR, feather_file)
    
    if not os.path.exists(file_path):
        print(f"⚠️  File not found: {feather_file} — Skipping")
        return None
    
    # Load feather file
    df = pd.read_feather(file_path)
    
    if 'stay_id' not in df.columns:
        print(f"⚠️  No stay_id in {feather_file} — Skipping")
        return None
    
    # Clean ID columns
    df = clean_id_columns(df)
    
    # Rename value column if needed
    if 'valuenum' in df.columns:
        df = df.rename(columns={'valuenum': new_col_name})
    
    if new_col_name not in df.columns:
        print(f"⚠️  Column '{new_col_name}' not found in {feather_file} — Skipping")
        return None
    
    # Keep only necessary columns
    keep_cols = ['stay_id', new_col_name]
    df = df[keep_cols].dropna(subset=['stay_id'])
    
    # Keep one value per stay (first measurement within 24h window)
    df = df.drop_duplicates(subset=['stay_id'], keep='first')
    
    return df


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """
    Main execution function.
    """
    print("=" * 70)
    print("MIMIC-IV Dataset Merging")
    print("=" * 70)
    
    # Initialize base file
    initialize_base_file()
    
    # Process and merge each variable file
    print("\n" + "=" * 70)
    print("MERGING VARIABLE FILES")
    print("=" * 70)
    
    for feather_file, new_col_name in VARIABLE_RENAME_MAP.items():
        print(f"\nProcessing: {feather_file}")
        
        # Load and prepare variable data
        df = process_variable_file(feather_file, new_col_name)
        
        if df is None:
            continue
        
        print(f"  {len(df):,} unique stays with {new_col_name} data")
        
        # Merge into progressive file
        merge_in_chunks(OUTPUT_CSV, df)
        
        # Report current file size
        sample = pd.read_csv(OUTPUT_CSV, dtype=str, nrows=10)
        print(f"  ✅ Merged — Progressive file now has {len(sample.columns)} columns")
    
    # Final summary
    print("\n" + "=" * 70)
    print("MERGE COMPLETE")
    print("=" * 70)
    
    final_df = pd.read_csv(OUTPUT_CSV, dtype=str, nrows=0)  # Just get column names
    print(f"Final dataset columns: {list(final_df.columns)}")
    print(f"Output saved to: {OUTPUT_CSV}")
    print("\nNext step: Run 03_calculate_scores.py to compute SOFA and APACHE II scores")


if __name__ == '__main__':
    main()
