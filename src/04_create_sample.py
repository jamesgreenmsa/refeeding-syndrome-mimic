"""
Sample Dataset Creation (Optional)
==================================

Create a random sample of the full dataset for testing or validation.

Author: James Green (jg1984@shp.rutgers.edu)
Created: 2024-10-17
Updated: 2025-11-06 (Documentation and cleanup for public release)

Description:
-----------
This optional script creates a random sample of N stays from the full dataset.
Useful for:
- Testing analysis code with smaller dataset
- Creating validation subsets
- Sharing de-identified sample data for code review

Input Files:
-----------
- sofa_apache_scores.csv: Full dataset with scores

Output Files:
------------
- sample_sofa_apache_scores.csv: Random sample of stays

Usage:
------
    python 04_create_sample.py
    
    Or with custom sample size:
    python 04_create_sample.py --sample_size 200
"""

import pandas as pd
import os
import argparse

# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_PATH = '/path/to/mimic-iv/'  # UPDATE THIS PATH
FULL_FILE = os.path.join(BASE_PATH, 'sofa_apache_scores.csv')
OUTPUT_FILE = os.path.join(BASE_PATH, 'sample_sofa_apache_scores.csv')
DEFAULT_SAMPLE_SIZE = 100
CHUNK_SIZE = 100000
RANDOM_SEED = 42  # For reproducibility

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def create_sample(sample_size: int = DEFAULT_SAMPLE_SIZE,
                 random_seed: int = RANDOM_SEED) -> None:
    """
    Create random sample from full dataset.
    
    Parameters:
    ----------
    sample_size : int
        Number of stays to sample
    random_seed : int
        Random seed for reproducibility
    """
    print("=" * 70)
    print("SAMPLE DATASET CREATION")
    print("=" * 70)
    print(f"Sample size: {sample_size}")
    print(f"Random seed: {random_seed}")
    
    # Step 1: Get unique stay_ids
    print("\n📊 Scanning file for unique stay_ids...")
    stay_ids = pd.read_csv(FULL_FILE, usecols=['stay_id'], dtype=str)
    
    unique_stays = stay_ids['stay_id'].dropna().drop_duplicates()
    print(f"   Found {len(unique_stays):,} unique stays")
    
    if sample_size > len(unique_stays):
        print(f"⚠️  Requested sample size ({sample_size}) exceeds available stays")
        print(f"   Using all {len(unique_stays)} stays instead")
        sample_size = len(unique_stays)
    
    # Step 2: Random sample of stay_ids
    print(f"\n🎲 Selecting {sample_size} random stays...")
    sample_stays = unique_stays.sample(n=sample_size, random_state=random_seed).tolist()
    sample_set = set(sample_stays)
    print(f"   ✅ Selected {len(sample_set)} stays")
    
    # Step 3: Filter full file in chunks
    print("\n📦 Reading full file in chunks and filtering...")
    chunks = pd.read_csv(FULL_FILE, dtype=str, chunksize=CHUNK_SIZE)
    matched_chunks = []
    
    for i, chunk in enumerate(chunks, 1):
        matched = chunk[chunk['stay_id'].isin(sample_set)]
        if not matched.empty:
            matched_chunks.append(matched)
        print(f"   Chunk {i} processed — {len(matched)} rows matched")
    
    # Step 4: Combine and save
    print("\n💾 Saving sample file...")
    final_sample = pd.concat(matched_chunks, ignore_index=True)
    final_sample.to_csv(OUTPUT_FILE, index=False)
    
    print("\n" + "=" * 70)
    print("SAMPLE CREATION COMPLETE")
    print("=" * 70)
    print(f"Sample size: {len(final_sample):,} rows ({sample_size} unique stays)")
    print(f"Output saved to: {OUTPUT_FILE}")


def main():
    """
    Main execution with argument parsing.
    """
    parser = argparse.ArgumentParser(
        description='Create random sample from SOFA/APACHE dataset'
    )
    parser.add_argument(
        '--sample_size',
        type=int,
        default=DEFAULT_SAMPLE_SIZE,
        help=f'Number of stays to sample (default: {DEFAULT_SAMPLE_SIZE})'
    )
    parser.add_argument(
        '--random_seed',
        type=int,
        default=RANDOM_SEED,
        help=f'Random seed for reproducibility (default: {RANDOM_SEED})'
    )
    
    args = parser.parse_args()
    
    create_sample(sample_size=args.sample_size, random_seed=args.random_seed)


if __name__ == '__main__':
    main()
