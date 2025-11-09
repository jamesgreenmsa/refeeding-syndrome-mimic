# Quick Start Guide

Get up and running with the refeeding syndrome MIMIC-IV analysis pipeline in 30 minutes.

## Prerequisites Checklist

- [ ] Python 3.8 or higher installed
- [ ] MIMIC-IV access approved via PhysioNet
- [ ] MIMIC-IV data downloaded to your computer
- [ ] Cohort definition file prepared (Excel with subject_id, hadm_id, stay_id)

**Don't have MIMIC-IV access yet?** See [docs/mimic_setup.md](docs/mimic_setup.md)

## Installation (5 minutes)

```bash
# Clone this repository
git clone https://github.com/[username]/refeeding-syndrome-mimic.git
cd refeeding-syndrome-mimic

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration (5 minutes)

Edit `config.py` and update these lines:

```python
# Line 8: Point to your MIMIC-IV data directory
BASE_PATH = '/path/to/your/mimic-iv-data'

# Line 11: Your cohort definition file
COHORT_FILE = 'your_cohort_file.xlsx'
```

Validate configuration:
```bash
python config.py
```

Should output:
```
✅ All required paths exist
✅ Output directories ready
```

## Run Pipeline (Variable time: 6-12 hours)

### Option 1: Run Complete Pipeline
```bash
python examples/pipeline_example.py
```

### Option 2: Run Step-by-Step
```bash
# Step 1: Extract variables (2-4 hours)
python src/01_extract_variables.py

# Step 2: Merge datasets (10-30 minutes)
python src/02_merge_datasets.py

# Step 3: Calculate scores (5-10 minutes)
python src/03_calculate_scores.py

# Step 4: Add patient info (2-5 minutes)
python src/05_add_patient_info.py
```

## Expected Outputs

Final dataset will be saved to:
```
[YOUR_BASE_PATH]/output_files/sofa_apache_full_with_info.csv
```

This file contains:
- Patient identifiers (subject_id, hadm_id, stay_id)
- SOFA scores (total and components)
- APACHE II scores
- Raw clinical values
- Medical history variables

## Quick Verification

Check your output file:
```python
import pandas as pd
df = pd.read_csv('[YOUR_BASE_PATH]/output_files/sofa_apache_full_with_info.csv')

print(f"Total patients: {df['stay_id'].nunique()}")
print(f"Columns: {list(df.columns)}")
print(f"SOFA score range: {df['sofa_score'].min()} - {df['sofa_score'].max()}")
```

## Common Issues

### "File not found" error
**Fix:** Check paths in `config.py` - use absolute paths

### "Out of memory" error  
**Fix:** In `config.py`, reduce `CHUNK_SIZE` from 100000 to 50000

### "Module not found" error
**Fix:** Activate virtual environment: `source venv/bin/activate`

### Very slow processing
**Fix:** Normal for large files - `chartevents.csv` takes hours. Run overnight.

## Next Steps

Once pipeline completes:

1. **Review data quality:**
   ```python
   import pandas as pd
   df = pd.read_csv('[OUTPUT_PATH]/sofa_apache_full_with_info.csv')
   
   # Check missing data
   print(df.isnull().sum())
   
   # Summary statistics
   print(df.describe())
   ```

2. **Perform your statistical analysis**

3. **Generate tables and figures**

4. **Cite this repository in your manuscript:**
   ```
   Green J, [PI Name]. Refeeding Syndrome Identification in ICU 
   Patients Using MIMIC-IV [Software]. GitHub; 2025. 
   Available from: https://github.com/[username]/refeeding-syndrome-mimic
   ```

## Getting Help

- **Documentation:** See `docs/` folder for detailed guides
- **Issues:** Open issue on GitHub
- **Email:** jg1984@shp.rutgers.edu

## Full Documentation

- [README.md](README.md) - Complete overview
- [docs/mimic_setup.md](docs/mimic_setup.md) - MIMIC-IV access guide
- [docs/data_dictionary.md](docs/data_dictionary.md) - Variable definitions
- [docs/methodology.md](docs/methodology.md) - Detailed methods
- [docs/manuscript_methods_template.md](docs/manuscript_methods_template.md) - Paper text

---

**Need more help?** Start with [README.md](README.md) for comprehensive documentation.
