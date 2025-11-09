"""
SOFA and APACHE II Score Calculation
====================================

Calculate Sequential Organ Failure Assessment (SOFA) and APACHE II scores
for ICU patients based on clinical measurements.

Author: James Green (jg1984@shp.rutgers.edu)
Created: 2024-10-17
Updated: 2025-11-06 (Documentation and cleanup for public release)

Description:
-----------
This script calculates severity of illness scores using extracted clinical
variables. SOFA score evaluates six organ systems; APACHE II provides acute
physiology assessment.

Input Files:
-----------
- progressive_merge.csv: Merged clinical variables
- cohort_definition.xlsx: Cohort information
- past_medical_history_full.csv: Medical history (optional)

Output Files:
------------
- sofa_apache_scores.csv: Dataset with calculated scores

References:
----------
- SOFA: Vincent JL, et al. Intensive Care Med. 1996;22(7):707-710.
- APACHE II: Knaus WA, et al. Crit Care Med. 1985;13(10):818-829.

Usage:
------
    python 03_calculate_scores.py
"""

import pandas as pd
import numpy as np
import os
from typing import Union

# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_PATH = '/path/to/mimic-iv/'  # UPDATE THIS PATH
COHORT_FILE = '31May 2025 Scrubbing.xlsx'  # UPDATE FILENAME AS NEEDED
PROGRESSIVE_CSV = os.path.join(BASE_PATH, 'temp_merge_files', 'progressive_merge.csv')
HISTORY_CSV = os.path.join(BASE_PATH, 'past_medical_history_full.csv')
OUTPUT_CSV = os.path.join(BASE_PATH, 'sofa_apache_scores.csv')

# =============================================================================
# SOFA SCORING FUNCTIONS
# =============================================================================

def score_platelet(platelet: float) -> int:
    """
    SOFA coagulation component based on platelet count.
    
    Parameters:
    ----------
    platelet : float
        Platelet count (×10³/μL)
    
    Returns:
    -------
    int
        Score from 0-4
    """
    if pd.isnull(platelet):
        return 0
    if platelet < 20:
        return 4
    elif platelet < 50:
        return 3
    elif platelet < 100:
        return 2
    elif platelet < 150:
        return 1
    else:
        return 0


def score_bilirubin(bilirubin: float) -> int:
    """
    SOFA liver component based on total bilirubin.
    
    Parameters:
    ----------
    bilirubin : float
        Total bilirubin (mg/dL)
    
    Returns:
    -------
    int
        Score from 0-4
    """
    if pd.isnull(bilirubin):
        return 0
    if bilirubin > 12.0:
        return 4
    elif bilirubin > 6.0:
        return 3
    elif bilirubin > 2.0:
        return 2
    elif bilirubin >= 1.2:
        return 1
    else:
        return 0


def score_creatinine_sofa(creatinine: float) -> int:
    """
    SOFA renal component based on creatinine.
    
    Parameters:
    ----------
    creatinine : float
        Serum creatinine (mg/dL)
    
    Returns:
    -------
    int
        Score from 0-4
    """
    if pd.isnull(creatinine):
        return 0
    if creatinine > 5.0:
        return 4
    elif creatinine >= 3.5:
        return 3
    elif creatinine >= 2.0:
        return 2
    elif creatinine >= 1.2:
        return 1
    else:
        return 0


def score_gcs(gcs_total: float) -> int:
    """
    SOFA neurological component based on Glasgow Coma Scale.
    
    Parameters:
    ----------
    gcs_total : float
        Total GCS score (range: 3-15)
    
    Returns:
    -------
    int
        Score from 0-4
    """
    if pd.isnull(gcs_total):
        return 0
    if gcs_total < 6:
        return 4
    elif gcs_total < 10:
        return 3
    elif gcs_total < 13:
        return 2
    elif gcs_total < 15:
        return 1
    else:
        return 0


def score_pf_ratio(pf_ratio: float) -> int:
    """
    SOFA respiratory component based on PaO₂/FiO₂ ratio.
    
    Parameters:
    ----------
    pf_ratio : float
        PaO₂/FiO₂ ratio (mmHg)
    
    Returns:
    -------
    int
        Score from 0-4
    """
    if pd.isnull(pf_ratio):
        return 0
    if pf_ratio < 100:
        return 4
    elif pf_ratio < 200:
        return 3
    elif pf_ratio < 300:
        return 2
    elif pf_ratio < 400:
        return 1
    else:
        return 0


def score_sofa_cardio(row: pd.Series) -> int:
    """
    SOFA cardiovascular component based on vasopressor use.
    
    Note: This is a simplified version. Full SOFA cardiovascular scoring
    requires detailed vasopressor dosing information.
    
    Parameters:
    ----------
    row : pd.Series
        Row containing sofa_cardio column if available
    
    Returns:
    -------
    int
        Score from 0-4
    """
    try:
        if 'sofa_cardio' in row and not pd.isnull(row['sofa_cardio']):
            return int(float(row['sofa_cardio']))
    except (ValueError, TypeError):
        pass
    return 0


# =============================================================================
# APACHE II SCORING FUNCTIONS
# =============================================================================

def score_temperature_apache(temperature: float) -> int:
    """
    APACHE II temperature component.
    
    Parameters:
    ----------
    temperature : float
        Temperature (Celsius)
    
    Returns:
    -------
    int
        Score from 0-4
    """
    if pd.isnull(temperature):
        return 0
    if temperature >= 41 or temperature <= 29.9:
        return 4
    elif temperature >= 39 or temperature <= 31.9:
        return 3
    elif temperature >= 38.5 or (temperature >= 30 and temperature <= 33.9):
        return 2
    elif (temperature >= 34 and temperature <= 35.9):
        return 1
    else:
        return 0


def score_creatinine_apache(creatinine: float) -> int:
    """
    APACHE II creatinine component.
    
    Parameters:
    ----------
    creatinine : float
        Serum creatinine (mg/dL)
    
    Returns:
    -------
    int
        Score from 0-4
    """
    if pd.isnull(creatinine):
        return 0
    if creatinine >= 3.5:
        return 4
    elif creatinine >= 2.0:
        return 3
    elif creatinine >= 1.5:
        return 2
    elif creatinine >= 0.6:
        return 0
    else:
        return 2


# =============================================================================
# DATA PROCESSING
# =============================================================================

def calculate_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate SOFA and APACHE II scores from clinical variables.
    
    Parameters:
    ----------
    df : pd.DataFrame
        DataFrame with clinical variables
    
    Returns:
    -------
    pd.DataFrame
        DataFrame with added score columns
    """
    print("Calculating severity scores...")
    
    # Ensure GCS columns exist
    gcs_cols = ['gcs_eye', 'gcs_motor', 'gcs_verbal']
    for col in gcs_cols:
        if col not in df.columns:
            df[col] = pd.NA
    
    # Calculate total GCS
    df['gcs_total'] = (
        df[gcs_cols]
        .apply(pd.to_numeric, errors='coerce')
        .sum(axis=1, min_count=1)
    )
    
    # Convert clinical variables to numeric
    df['fio2_fraction'] = pd.to_numeric(df.get('fio2', pd.NA), errors='coerce') / 100
    df['pao2'] = pd.to_numeric(df.get('pao2', pd.NA), errors='coerce')
    df['pf_ratio'] = df['pao2'] / df['fio2_fraction']
    df['platelet'] = pd.to_numeric(df.get('platelet', pd.NA), errors='coerce')
    df['bilirubin'] = pd.to_numeric(df.get('bilirubin', pd.NA), errors='coerce')
    df['creatinine'] = pd.to_numeric(df.get('creatinine', pd.NA), errors='coerce')
    df['temperature'] = pd.to_numeric(df.get('temperature', pd.NA), errors='coerce')
    
    # Calculate SOFA components
    df['sofa_platelet'] = df['platelet'].apply(score_platelet)
    df['sofa_bilirubin'] = df['bilirubin'].apply(score_bilirubin)
    df['sofa_creatinine'] = df['creatinine'].apply(score_creatinine_sofa)
    df['sofa_gcs'] = df['gcs_total'].apply(score_gcs)
    df['sofa_pf'] = df['pf_ratio'].apply(score_pf_ratio)
    df['sofa_cardio_score'] = df.apply(score_sofa_cardio, axis=1)
    
    # Calculate total SOFA score
    sofa_components = [
        'sofa_platelet', 'sofa_bilirubin', 'sofa_creatinine',
        'sofa_gcs', 'sofa_pf', 'sofa_cardio_score'
    ]
    df['sofa_score'] = df[sofa_components].sum(axis=1)
    
    # Calculate APACHE II components (simplified version)
    df['apache_creatinine'] = df['creatinine'].apply(score_creatinine_apache)
    df['apache_temp'] = df['temperature'].apply(score_temperature_apache)
    df['apache_score'] = df[['apache_creatinine', 'apache_temp']].sum(axis=1)
    
    print(f"✅ Scores calculated for {len(df):,} stays")
    print(f"   SOFA score range: {df['sofa_score'].min():.0f} - {df['sofa_score'].max():.0f}")
    print(f"   APACHE score range: {df['apache_score'].min():.0f} - {df['apache_score'].max():.0f}")
    
    return df


def merge_medical_history(df: pd.DataFrame, history_path: str) -> pd.DataFrame:
    """
    Merge patient medical history if available.
    
    Parameters:
    ----------
    df : pd.DataFrame
        Main dataset
    history_path : str
        Path to medical history CSV
    
    Returns:
    -------
    pd.DataFrame
        Dataset with medical history added
    """
    if not os.path.exists(history_path):
        print("⚠️  Medical history file not found — continuing without it")
        return df
    
    print("Merging medical history...")
    
    history_df = pd.read_csv(history_path, dtype=str)
    
    # Clean ID columns
    for key in ['subject_id', 'hadm_id', 'stay_id']:
        history_df[key] = (
            history_df[key]
            .astype(str)
            .str.strip()
            .str.replace('.0', '', regex=False)
        )
    
    # Define medical history columns to include
    history_cols = [
        'subject_id', 'hadm_id', 'stay_id',
        'ANEMIA', 'ASTHMA', 'COPD', 'DIABETES - INSULIN',
        'DIABETES - ORAL AGENT', 'ETOH', 'GI BLEED',
        'HEMO OR PD', 'HEPATITIS', 'LIVER FAILURE',
        'PANCREATITIS', 'RENAL FAILURE', 'SEIZURES', 'SMOKER'
    ]
    
    # Keep only available columns
    available_cols = [col for col in history_cols if col in history_df.columns]
    
    # Merge
    df = df.merge(
        history_df[available_cols],
        on=['subject_id', 'hadm_id', 'stay_id'],
        how='left'
    )
    
    print(f"✅ Medical history merged ({len(available_cols) - 3} conditions)")
    
    return df


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """
    Main execution function.
    """
    print("=" * 70)
    print("SOFA and APACHE II Score Calculation")
    print("=" * 70)
    
    # Load merged dataset
    print(f"Loading merged dataset: {PROGRESSIVE_CSV}")
    df = pd.read_csv(PROGRESSIVE_CSV, on_bad_lines='skip')
    print(f"✅ Loaded {len(df):,} rows")
    
    # Load cohort information
    print(f"\nLoading cohort information: {COHORT_FILE}")
    scrub_df = pd.read_excel(
        os.path.join(BASE_PATH, COHORT_FILE),
        sheet_name='Data File',
        dtype=str
    )
    scrub_df = scrub_df[['subject_id', 'hadm_id', 'stay_id']].drop_duplicates()
    
    # Clean ID columns
    df['stay_id'] = (
        df['stay_id']
        .astype(str)
        .str.strip()
        .str.replace('.0', '', regex=False)
    )
    scrub_df['stay_id'] = (
        scrub_df['stay_id']
        .astype(str)
        .str.strip()
        .str.replace('.0', '', regex=False)
    )
    
    # Calculate scores
    print("\n" + "=" * 70)
    print("CALCULATING SCORES")
    print("=" * 70)
    df = calculate_scores(df)
    
    # Merge with cohort to ensure correct stay definitions
    print("\nMerging with cohort definition...")
    scores = df.drop(columns=['subject_id', 'hadm_id'], errors='ignore')
    scores = scrub_df.merge(scores, on='stay_id', how='left')
    
    # Add medical history if available
    print("\n" + "=" * 70)
    print("ADDING MEDICAL HISTORY")
    print("=" * 70)
    scores = merge_medical_history(scores, HISTORY_CSV)
    
    # Define output columns
    output_cols = [
        # Identifiers
        'subject_id', 'hadm_id', 'stay_id',
        # Severity scores
        'sofa_score', 'apache_score',
        # SOFA components
        'sofa_platelet', 'platelet',
        'sofa_bilirubin', 'bilirubin',
        'sofa_creatinine', 'creatinine',
        'sofa_gcs', 'gcs_eye', 'gcs_motor', 'gcs_verbal', 'gcs_total',
        'sofa_pf', 'pao2', 'fio2', 'fio2_fraction', 'pf_ratio',
        'sofa_cardio_score',
        # APACHE components
        'apache_creatinine', 'apache_temp', 'temperature',
        # Medical history
        'ANEMIA', 'ASTHMA', 'COPD', 'DIABETES - INSULIN',
        'DIABETES - ORAL AGENT', 'ETOH', 'GI BLEED', 'HEMO OR PD',
        'HEPATITIS', 'LIVER FAILURE', 'PANCREATITIS', 'RENAL FAILURE',
        'SEIZURES', 'SMOKER'
    ]
    
    # Add missing columns as NA
    for col in output_cols:
        if col not in scores.columns:
            scores[col] = pd.NA
    
    # Save output
    scores[output_cols].to_csv(OUTPUT_CSV, index=False)
    
    print("\n" + "=" * 70)
    print("SCORE CALCULATION COMPLETE")
    print("=" * 70)
    print(f"Output saved to: {OUTPUT_CSV}")
    print(f"Total stays: {len(scores):,}")
    print(f"Variables included: {len(output_cols)}")
    print("\nNext step: Run 05_add_patient_info.py to add demographics")


if __name__ == '__main__':
    main()
