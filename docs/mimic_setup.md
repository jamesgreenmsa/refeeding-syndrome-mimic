# MIMIC-IV Access and Setup Guide

## Overview

This guide walks you through obtaining access to the MIMIC-IV database and setting up your environment to run the refeeding syndrome analysis pipeline.

## Step 1: Complete Required Training

Before accessing MIMIC-IV data, you must complete CITI training:

1. Go to https://about.citiprogram.org/
2. Register for an account (if you don't have one)
3. Complete the course: **"Data or Specimens Only Research"**
4. Save your completion certificate (you'll need to upload it)

**Time required:** Approximately 2-3 hours

## Step 2: Create PhysioNet Account

1. Visit https://physionet.org/
2. Click "Register" in the top right
3. Complete the registration form:
   - Use your institutional email address
   - Provide accurate information (verified against training certificate)
4. Verify your email address

## Step 3: Request Access to MIMIC-IV

1. Log in to PhysioNet
2. Navigate to: https://physionet.org/content/mimiciv/
3. Click "Files" tab
4. Click "Request Access" button
5. Complete the credentialing application:
   - Upload CITI training certificate
   - Agree to Data Use Agreement
   - Provide research supervisor information (if applicable)
   - Describe your research project

**Processing time:** Typically 1-7 days for approval

### Data Use Agreement Key Points

By accessing MIMIC-IV, you agree to:
- Use data only for research purposes
- Not attempt to re-identify patients
- Report any inadvertent re-identification
- Cite the database in publications
- Share analysis code publicly (this repository fulfills that requirement)

## Step 4: Download MIMIC-IV Data

Once approved, you can download the data:

### Option A: Direct Download (Recommended for Full Dataset)

1. Log in to PhysioNet
2. Go to MIMIC-IV page: https://physionet.org/content/mimiciv/
3. Click "Files" tab
4. Download required modules:

**For this analysis, you need:**

**Core Module** (~45 GB compressed):
- `hosp/patients.csv` - Patient demographics
- `hosp/admissions.csv` - Hospital admissions
- `hosp/labevents.csv` - **LARGE FILE** (~22 GB) - Laboratory results
- `hosp/icustays.csv` - ICU stay information

**ICU Module** (~23 GB compressed):
- `icu/chartevents.csv` - **VERY LARGE FILE** (~40 GB) - Vital signs and assessments
- `icu/icustays.csv` - ICU stay details (duplicate, but good backup)

**Optional but Recommended:**
- `hosp/diagnoses_icd.csv` - ICD diagnosis codes
- `hosp/procedures_icd.csv` - ICD procedure codes
- Medical history files (if available)

### Option B: wget (Command Line)

```bash
# Create directory for MIMIC-IV data
mkdir -p ~/mimic-iv/data
cd ~/mimic-iv/data

# Download files using wget (requires PhysioNet credentials)
wget -r -N -c -np --user YOUR_USERNAME --ask-password \
  https://physionet.org/files/mimiciv/2.0/
```

Replace `YOUR_USERNAME` with your PhysioNet username.

### Option C: Google Cloud Platform (Fastest for Large Dataset)

MIMIC-IV is available on Google Cloud Platform for faster access:

1. Visit: https://mimic.mit.edu/docs/gettingstarted/cloud/
2. Follow instructions to access via Google Cloud
3. Either:
   - Work directly in cloud (requires GCP account)
   - Download to local machine from GCP (faster than direct download)

**Advantages:**
- Much faster download speeds
- Can analyze directly in cloud
- No local storage requirements

**Disadvantages:**
- Requires Google Cloud account
- May incur cloud computing costs
- Need to learn cloud workflows

## Step 5: Extract and Organize Data

After downloading, organize your files:

```bash
# Recommended directory structure
~/mimic-iv/
├── data/
│   ├── hosp/
│   │   ├── patients.csv
│   │   ├── admissions.csv
│   │   ├── labevents.csv
│   │   └── ...
│   └── icu/
│       ├── chartevents.csv
│       ├── icustays.csv
│       └── ...
├── refeeding-syndrome-mimic/  # This repository
│   ├── src/
│   ├── config.py
│   └── ...
└── output/  # Will be created by scripts
```

**Unzip files if compressed:**
```bash
cd ~/mimic-iv/data
gunzip hosp/*.gz
gunzip icu/*.gz
```

## Step 6: Prepare Your Cohort Definition

Create your cohort definition file (Excel format):

**Required columns:**
- `subject_id` - Patient identifier
- `hadm_id` - Hospital admission identifier  
- `stay_id` - ICU stay identifier

**Example:**
```
subject_id | hadm_id | stay_id
10000032   | 29079034| 39553978
10000084   | 26913865| 39765666
...
```

Save as: `cohort_definition.xlsx` in your MIMIC-IV data directory.

## Step 7: Set Up Python Environment

### Install Python (if needed)

**Option A: Anaconda (Recommended)**
```bash
# Download Anaconda
wget https://repo.anaconda.com/archive/Anaconda3-latest-Linux-x86_64.sh

# Install
bash Anaconda3-latest-Linux-x86_64.sh

# Create environment for this project
conda create -n refeeding python=3.9
conda activate refeeding
```

**Option B: System Python**
```bash
# Ensure Python 3.8+ is installed
python3 --version

# Create virtual environment
python3 -m venv ~/refeeding-env
source ~/refeeding-env/bin/activate  # Linux/Mac
# OR
~/refeeding-env/Scripts/activate  # Windows
```

### Install Required Packages

```bash
# Navigate to repository
cd ~/mimic-iv/refeeding-syndrome-mimic

# Install dependencies
pip install -r requirements.txt
```

## Step 8: Configure the Pipeline

Edit `config.py` to point to your data location:

```python
# Update these paths
BASE_PATH = '/Users/yourname/mimic-iv/data'  # Your MIMIC-IV location
COHORT_FILE = 'cohort_definition.xlsx'        # Your cohort file
```

Validate your configuration:
```bash
python config.py
```

Should output:
```
✅ All required paths exist
✅ Output directories ready
```

## Step 9: Test Your Setup

Run a quick test to ensure everything works:

```bash
# Test with sample data (if available)
python src/04_create_sample.py --sample_size 10

# Or test configuration only
python -c "import pandas as pd; import config; print('Setup OK!')"
```

## Common Issues and Solutions

### Issue: "File not found" errors

**Solution:**
- Check file paths in `config.py`
- Ensure files are unzipped
- Verify file permissions: `ls -l ~/mimic-iv/data/hosp/`

### Issue: Out of memory errors

**Solution:**
- Reduce `CHUNK_SIZE` in `config.py` (try 50000 instead of 100000)
- Close other applications
- Consider cloud-based processing
- Use machine with more RAM (recommended: 16+ GB)

### Issue: PhysioNet access denied

**Solution:**
- Check that CITI training is complete and certificate uploaded
- Verify your application was approved (check email)
- Wait 1-7 days after application
- Contact PhysioNet support: https://physionet.org/about/

### Issue: Slow processing on chartevents.csv

**Solution:**
- This file is ~40 GB and will take time (potentially hours)
- Ensure adequate disk space (at least 100 GB free)
- Consider running overnight
- Cloud processing may be faster

### Issue: Missing medical history file

**Solution:**
- This file is optional
- Script will continue without it (with warning message)
- Create if needed from MIMIC-IV diagnosis tables

## Storage Requirements

**Minimum disk space needed:**
- Raw MIMIC-IV data: ~150 GB (uncompressed)
- Working space for processing: ~50 GB
- Output files: ~5 GB
- **Total: ~205 GB**

**Recommended:** 250+ GB free disk space

## Performance Expectations

Processing times (approximate, on standard laptop):

| Step | File Size | Expected Time |
|------|-----------|---------------|
| Extract labs | ~22 GB | 2-4 hours |
| Extract charts | ~40 GB | 4-8 hours |
| Merge datasets | ~1 GB | 10-30 minutes |
| Calculate scores | ~500 MB | 5-10 minutes |
| Add patient info | ~500 MB | 2-5 minutes |

**Total pipeline runtime:** 6-12 hours

**Ways to speed up:**
- Use machine with SSD (vs. HDD)
- Increase RAM
- Use cloud computing
- Process smaller cohort

## Next Steps

Once setup is complete:

1. Review the [Methodology](methodology.md) documentation
2. Customize `config.py` for your specific study
3. Prepare your cohort definition file
4. Run the pipeline:
   ```bash
   python src/01_extract_variables.py
   python src/02_merge_datasets.py
   python src/03_calculate_scores.py
   python src/05_add_patient_info.py
   ```

5. Review output files in your output directory

## Getting Help

**MIMIC-IV specific questions:**
- Documentation: https://mimic.mit.edu/
- Forum: https://github.com/MIT-LCP/mimic-code/discussions
- Email: mimic-support@physionet.org

**Code/pipeline questions:**
- GitHub Issues: [Repository URL]/issues
- Email: jg1984@shp.rutgers.edu

## Additional Resources

**MIMIC-IV Documentation:**
- Official docs: https://mimic.mit.edu/docs/iv/
- Schema browser: https://mit-lcp.github.io/mimic-schema-spy/
- Example code: https://github.com/MIT-LCP/mimic-code

**Tutorials:**
- MIMIC-IV introduction: https://mimic.mit.edu/docs/iv/tutorials/intro/
- Querying MIMIC-IV: https://mimic.mit.edu/docs/iv/tutorials/bigquery/

**Papers using MIMIC:**
- PubMed search: https://pubmed.ncbi.nlm.nih.gov/?term=MIMIC

---

**Document Version:** 1.0  
**Last Updated:** November 6, 2025  
**Maintainer:** James Green (jg1984@shp.rutgers.edu)
