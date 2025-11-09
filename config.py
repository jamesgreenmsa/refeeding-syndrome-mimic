"""
Configuration File for MIMIC-IV Refeeding Syndrome Analysis
===========================================================

This file contains configuration settings for the data processing pipeline.
Update the paths and parameters to match your local environment.

Author: James Green (jg1984@shp.rutgers.edu)
"""

import os

# =============================================================================
# PATH CONFIGURATION
# =============================================================================

# Base path to MIMIC-IV data directory
# UPDATE THIS to point to your MIMIC-IV installation
BASE_PATH = '/path/to/mimic-iv/'

# Cohort definition file
# This file should contain subject_id, hadm_id, stay_id for your study cohort
COHORT_FILE = 'cohort_definition.xlsx'
COHORT_SHEET = 'Data File'

# Optional: Medical history file
HISTORY_FILE = 'past_medical_history_full.csv'

# Output directories
TEMP_DIR = os.path.join(BASE_PATH, 'temp_merge_files')
OUTPUT_DIR = os.path.join(BASE_PATH, 'output_files')

# =============================================================================
# PROCESSING PARAMETERS
# =============================================================================

# Chunk size for streaming large files (adjust based on available RAM)
CHUNK_SIZE = 100000

# Time window for measurements (hours from ICU admission)
TIME_WINDOW_HOURS = 24

# Random seed for reproducible sampling
RANDOM_SEED = 42

# =============================================================================
# MIMIC-IV TABLE PATHS
# =============================================================================

# Core MIMIC-IV tables
ICUSTAYS_PATH = os.path.join(BASE_PATH, 'icustays.csv')
LABEVENTS_PATH = os.path.join(BASE_PATH, 'labevents.csv')
CHARTEVENTS_PATH = os.path.join(BASE_PATH, 'chartevents.csv')

# Optional additional tables
PATIENTS_PATH = os.path.join(BASE_PATH, 'patients.csv')
ADMISSIONS_PATH = os.path.join(BASE_PATH, 'admissions.csv')

# =============================================================================
# MIMIC-IV ITEMID MAPPINGS
# =============================================================================

# Laboratory measurements
LAB_ITEMIDS = {
    'platelet': 51265,      # Platelet count (×10³/μL)
    'bilirubin': 50885,     # Total bilirubin (mg/dL)
    'creatinine': 50912,    # Creatinine (mg/dL)
    'pao2': 50821,         # PaO₂ (mmHg)
    'sodium': 50983,       # Sodium (mEq/L) - optional
    'potassium': 50971,    # Potassium (mEq/L) - optional
    'phosphate': 50970,    # Phosphate (mg/dL) - optional
    'magnesium': 50960     # Magnesium (mg/dL) - optional
}

# Chart events (vitals and assessments)
CHART_ITEMIDS = {
    'gcs_motor': 223901,    # Glasgow Coma Scale - Motor
    'gcs_verbal': 223900,   # Glasgow Coma Scale - Verbal
    'gcs_eye': 220739,      # Glasgow Coma Scale - Eye opening
    'temperature': 223761,  # Temperature (°C)
    'map': 220052,         # Mean arterial pressure (mmHg)
    'fio2': [223835, 3420] # Fraction inspired oxygen (%)
}

# =============================================================================
# SCORING PARAMETERS
# =============================================================================

# SOFA Score thresholds (based on Vincent et al., 1996)
SOFA_THRESHOLDS = {
    'platelet': [150, 100, 50, 20],           # ×10³/μL
    'bilirubin': [1.2, 2.0, 6.0, 12.0],       # mg/dL
    'creatinine': [1.2, 2.0, 3.5, 5.0],       # mg/dL
    'gcs': [15, 13, 10, 6],                    # Total score
    'pf_ratio': [400, 300, 200, 100],         # mmHg
}

# APACHE II thresholds (based on Knaus et al., 1985)
APACHE_THRESHOLDS = {
    'temperature': {  # °C
        4: [(41, float('inf')), (float('-inf'), 29.9)],
        3: [(39, 40.9), (30, 31.9)],
        2: [(38.5, 38.9), (32, 33.9)],
        1: [(34, 35.9)],
        0: [(36, 38.4)]
    },
    'creatinine': {  # mg/dL
        4: [(3.5, float('inf'))],
        3: [(2.0, 3.4)],
        2: [(1.5, 1.9), (0.0, 0.6)],
        0: [(0.6, 1.4)]
    }
}

# =============================================================================
# OUTPUT COLUMN DEFINITIONS
# =============================================================================

# Define order and selection of columns in final output
OUTPUT_COLUMNS = [
    # Identifiers
    'subject_id',
    'hadm_id',
    'stay_id',
    
    # Primary outcome scores
    'sofa_score',
    'apache_score',
    
    # SOFA components
    'sofa_platelet',
    'sofa_bilirubin',
    'sofa_creatinine',
    'sofa_gcs',
    'sofa_pf',
    'sofa_cardio_score',
    
    # APACHE components  
    'apache_creatinine',
    'apache_temp',
    
    # Raw clinical values
    'platelet',
    'bilirubin',
    'creatinine',
    'gcs_eye',
    'gcs_motor',
    'gcs_verbal',
    'gcs_total',
    'pao2',
    'fio2',
    'fio2_fraction',
    'pf_ratio',
    'temperature',
]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def validate_paths():
    """
    Validate that required paths exist.
    
    Returns:
    -------
    bool
        True if all required paths exist, False otherwise
    """
    required_paths = [
        BASE_PATH,
        os.path.join(BASE_PATH, COHORT_FILE),
        ICUSTAYS_PATH,
        LABEVENTS_PATH,
        CHARTEVENTS_PATH
    ]
    
    missing_paths = []
    for path in required_paths:
        if not os.path.exists(path):
            missing_paths.append(path)
    
    if missing_paths:
        print("❌ Missing required files:")
        for path in missing_paths:
            print(f"   - {path}")
        return False
    
    return True


def create_directories():
    """
    Create necessary output directories if they don't exist.
    """
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"✅ Output directories ready:")
    print(f"   - {TEMP_DIR}")
    print(f"   - {OUTPUT_DIR}")


if __name__ == '__main__':
    print("Configuration Validation")
    print("=" * 70)
    
    if validate_paths():
        print("✅ All required paths exist")
        create_directories()
    else:
        print("\n⚠️  Please update config.py with correct paths before running pipeline")
