"""
Complete Pipeline Example
=========================

This script demonstrates running the complete data processing pipeline
for the refeeding syndrome MIMIC-IV analysis.

Author: James Green (jg1984@shp.rutgers.edu)
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import pipeline modules
import config
from src import (
    extract_variables,
    merge_datasets,
    calculate_scores,
    add_patient_info
)

def run_pipeline():
    """
    Execute the complete data processing pipeline.
    """
    print("=" * 70)
    print("REFEEDING SYNDROME MIMIC-IV ANALYSIS PIPELINE")
    print("=" * 70)
    
    # Validate configuration
    print("\nStep 0: Validating configuration...")
    if not config.validate_paths():
        print("\n❌ Configuration validation failed!")
        print("Please update config.py with correct paths.")
        return False
    
    config.create_directories()
    
    # Step 1: Extract variables
    print("\n" + "=" * 70)
    print("STEP 1: EXTRACT CLINICAL VARIABLES")
    print("=" * 70)
    print("This may take several hours for large datasets...")
    
    try:
        extract_variables.main()
    except Exception as e:
        print(f"\n❌ Step 1 failed: {e}")
        return False
    
    # Step 2: Merge datasets
    print("\n" + "=" * 70)
    print("STEP 2: MERGE DATASETS")
    print("=" * 70)
    
    try:
        merge_datasets.main()
    except Exception as e:
        print(f"\n❌ Step 2 failed: {e}")
        return False
    
    # Step 3: Calculate scores
    print("\n" + "=" * 70)
    print("STEP 3: CALCULATE SOFA AND APACHE II SCORES")
    print("=" * 70)
    
    try:
        calculate_scores.main()
    except Exception as e:
        print(f"\n❌ Step 3 failed: {e}")
        return False
    
    # Step 4: Add patient information
    print("\n" + "=" * 70)
    print("STEP 4: ADD PATIENT INFORMATION")
    print("=" * 70)
    
    try:
        add_patient_info.main()
    except Exception as e:
        print(f"\n❌ Step 4 failed: {e}")
        return False
    
    # Success!
    print("\n" + "=" * 70)
    print("PIPELINE COMPLETE!")
    print("=" * 70)
    print(f"\nFinal dataset available at:")
    print(f"  {config.OUTPUT_DIR}/sofa_apache_full_with_info.csv")
    print("\nNext steps:")
    print("  1. Review data quality")
    print("  2. Perform descriptive analysis")
    print("  3. Conduct statistical analyses")
    print("  4. Generate tables and figures")
    
    return True


if __name__ == '__main__':
    success = run_pipeline()
    sys.exit(0 if success else 1)
