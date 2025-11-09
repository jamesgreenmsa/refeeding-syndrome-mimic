"""
Add Patient Demographics and Clinical Information
=================================================

Merge patient demographics and additional clinical information into the
final analytical dataset.

Author: James Green (jg1984@shp.rutgers.edu)
Created: 2024-10-17
Updated: 2025-11-06 (Documentation and cleanup for public release)

Description:
-----------
This script adds patient-level information (demographics, admission details,
etc.) from the cohort definition file to the dataset with calculated scores.

Input Files:
-----------
- sofa_apache_scores.csv: Dataset with calculated scores
- cohort_definition.xlsx: Full patient information

Output Files:
------------
- sofa_apache_full_with_info.csv: Complete analytical dataset

Usage:
------
    python 05_add_patient_info.py
"""

import pandas as pd
import os

# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_PATH = '/path/to/mimic-iv/'  # UPDATE THIS PATH
OUTPUT_PATH = os.path.join(BASE_PATH, 'output_files')

SCORES_CSV = os.path.join(BASE_PATH, 'sofa_apache_scores.csv')
COHORT_FILE = '31May 2025 Scrubbing.xlsx'  # UPDATE FILENAME AS NEEDED
OUTPUT_CSV = os.path.join(OUTPUT_PATH, 'sofa_apache_full_with_info.csv')

# Create output directory if needed
os.makedirs(OUTPUT_PATH, exist_ok=True)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def clean_id_columns(df: pd.DataFrame,
                    columns: list = None) -> pd.DataFrame:
    """
    Standardize ID column formats for merging.
    
    Parameters:
    ----------
    df : pd.DataFrame
        DataFrame with ID columns
    columns : list, optional
        List of columns to clean (default: subject_id, hadm_id, stay_id)
    
    Returns:
    -------
    pd.DataFrame
        DataFrame with cleaned columns
    """
    if columns is None:
        columns = ['subject_id', 'hadm_id', 'stay_id']
    
    for col in columns:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.replace('.0', '', regex=False)
            )
    
    return df


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """
    Main execution function.
    """
    print("=" * 70)
    print("ADD PATIENT INFORMATION TO ANALYTICAL DATASET")
    print("=" * 70)
    
    # Load scores dataset
    print(f"\n📂 Loading scores from: {SCORES_CSV}")
    scores_df = pd.read_csv(SCORES_CSV, dtype=str)
    print(f"   ✅ Loaded {len(scores_df):,} rows")
    print(f"   Columns: {len(scores_df.columns)}")
    
    # Load cohort information
    print(f"\n📂 Loading patient info from: {COHORT_FILE}")
    cohort_path = os.path.join(BASE_PATH, COHORT_FILE)
    scrub_df = pd.read_excel(cohort_path, sheet_name='Data File', dtype=str)
    print(f"   ✅ Loaded {len(scrub_df):,} rows")
    print(f"   Columns: {len(scrub_df.columns)}")
    
    # Clean and align merge keys
    print("\n🔧 Cleaning ID columns for merge...")
    scores_df = clean_id_columns(scores_df)
    scrub_df = clean_id_columns(scrub_df)
    
    # Identify patient info columns (exclude merge keys)
    merge_keys = ['subject_id', 'hadm_id', 'stay_id']
    patient_info_cols = [
        col for col in scrub_df.columns 
        if col not in merge_keys
    ]
    
    print(f"   Patient info columns to add: {len(patient_info_cols)}")
    if len(patient_info_cols) <= 20:  # Show if reasonable number
        print(f"   {', '.join(patient_info_cols)}")
    
    # Merge datasets
    print("\n🔀 Merging patient information...")
    merged_df = scores_df.merge(
        scrub_df[merge_keys + patient_info_cols],
        on=merge_keys,
        how='left'
    )
    
    # Check merge quality
    rows_with_info = merged_df[patient_info_cols].notna().any(axis=1).sum()
    print(f"   ✅ Merge complete")
    print(f"   Rows with patient info: {rows_with_info:,} ({rows_with_info/len(merged_df)*100:.1f}%)")
    
    # Save final dataset
    print(f"\n💾 Saving final dataset to: {OUTPUT_CSV}")
    merged_df.to_csv(OUTPUT_CSV, index=False)
    
    # Final summary
    print("\n" + "=" * 70)
    print("FINAL DATASET COMPLETE")
    print("=" * 70)
    print(f"Total rows: {len(merged_df):,}")
    print(f"Total columns: {len(merged_df.columns)}")
    print(f"Output location: {OUTPUT_CSV}")
    
    # Show column categories
    score_cols = [col for col in merged_df.columns if 'sofa' in col.lower() or 'apache' in col.lower()]
    clinical_cols = [col for col in merged_df.columns if any(x in col.lower() for x in ['platelet', 'bilirubin', 'creatinine', 'pao2', 'gcs', 'temperature'])]
    
    print("\nColumn summary:")
    print(f"   Identifiers: {len(merge_keys)}")
    print(f"   Severity scores: {len(score_cols)}")
    print(f"   Clinical variables: {len(clinical_cols)}")
    print(f"   Patient information: {len(patient_info_cols)}")
    
    print("\n✅ Dataset ready for analysis!")


if __name__ == '__main__':
    main()
