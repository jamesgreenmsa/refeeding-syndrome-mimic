# Refeeding Syndrome Identification in ICU Patients Using MIMIC-IV

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This repository contains the source code and data processing pipeline for identifying refeeding syndrome in critically ill patients using the MIMIC-IV (Medical Information Mart for Intensive Care) database. This work supports a doctoral research project examining refeeding syndrome predictors and outcomes in ICU settings.

**Publication Target:** Journal of Parenteral and Enteral Nutrition

## Study Description

Refeeding syndrome is a potentially life-threatening complication that can occur when nutrition is reintroduced to malnourished patients. This study analyzes ICU patient data to identify refeeding syndrome cases and associated risk factors using clinical scoring systems (SOFA, APACHE II) and laboratory values.

## Repository Structure

```
.
├── README.md                          # This file
├── LICENSE                            # MIT License
├── requirements.txt                   # Python dependencies
├── config.py                          # Configuration and paths
├── src/                              # Source code
│   ├── 01_extract_variables.py       # Extract clinical variables from MIMIC-IV
│   ├── 02_merge_datasets.py          # Merge extracted variables
│   ├── 03_calculate_scores.py        # Calculate SOFA and APACHE II scores
│   ├── 04_create_sample.py           # Create sample dataset (optional)
│   ├── 05_add_patient_info.py        # Add patient demographics
│   └── utils.py                      # Utility functions
├── docs/                             # Documentation
│   ├── data_dictionary.md            # Variable definitions
│   ├── methodology.md                # Detailed methodology
│   └── mimic_setup.md                # MIMIC-IV access instructions
└── examples/                         # Example usage
    └── pipeline_example.py           # Full pipeline example
```

## Requirements

### Data Access

This project requires access to the MIMIC-IV database:

1. Complete the CITI "Data or Specimens Only Research" training
2. Request access via PhysioNet: https://physionet.org/content/mimiciv/
3. Sign the Data Use Agreement
4. Download MIMIC-IV v2.0+ data files

See `docs/mimic_setup.md` for detailed instructions.

### Software Dependencies

- Python 3.8+
- pandas >= 1.3.0
- numpy >= 1.21.0
- openpyxl >= 3.0.0
- pyarrow >= 5.0.0 (for feather file support)

Install dependencies:
```bash
pip install -r requirements.txt
```

## Data Processing Pipeline

### Step 1: Extract Clinical Variables

Extract relevant clinical variables (lab values, vitals, GCS scores) from MIMIC-IV tables within the first 24 hours of ICU admission.

```bash
python src/01_extract_variables.py
```

**Inputs:**
- `icustays.csv` - ICU stay information
- `labevents.csv` - Laboratory measurements
- `chartevents.csv` - Vital signs and assessments
- Cohort definition file (Excel)

**Outputs:**
- Individual feather files for each variable in `temp_merge_files/`

### Step 2: Merge Datasets

Combine extracted variables into a single analytical dataset.

```bash
python src/02_merge_datasets.py
```

**Outputs:**
- `progressive_merge.csv` - Combined dataset with all variables

### Step 3: Calculate Severity Scores

Calculate SOFA (Sequential Organ Failure Assessment) and APACHE II scores.

```bash
python src/03_calculate_scores.py
```

**Outputs:**
- `sofa_apache_scores.csv` - Dataset with calculated severity scores

### Step 4: Add Patient Information

Merge patient demographics and medical history.

```bash
python src/05_add_patient_info.py
```

**Outputs:**
- `sofa_apache_full_with_info.csv` - Complete analytical dataset

### Optional: Create Sample Dataset

For testing or validation purposes, create a random sample:

```bash
python src/04_create_sample.py
```

## Clinical Variables Extracted

### SOFA Score Components
- **Respiratory:** PaO₂/FiO₂ ratio
- **Coagulation:** Platelet count
- **Hepatic:** Bilirubin
- **Cardiovascular:** Mean arterial pressure, vasopressor use
- **Neurological:** Glasgow Coma Scale (GCS)
- **Renal:** Creatinine

### APACHE II Components
- Temperature
- Creatinine
- (Additional physiologic variables as documented)

### Medical History
- Chronic conditions (diabetes, COPD, liver disease, etc.)
- Substance use history (alcohol, smoking)
- Previous dialysis

See `docs/data_dictionary.md` for complete variable definitions and MIMIC-IV itemid mappings.

## Scoring Methodology

### SOFA Score (Range: 0-24)

The SOFA score evaluates six organ systems. Thresholds used:

| Component | Score | Criteria |
|-----------|-------|----------|
| Respiration | 0-4 | PaO₂/FiO₂ ≥400 to <100 |
| Coagulation | 0-4 | Platelets ≥150 to <20 (×10³/μL) |
| Liver | 0-4 | Bilirubin <1.2 to >12 mg/dL |
| Cardiovascular | 0-4 | MAP ≥70 to vasopressor use |
| CNS | 0-4 | GCS 15 to <6 |
| Renal | 0-4 | Creatinine <1.2 to >5.0 mg/dL |

### APACHE II Score

Simplified components extracted from MIMIC-IV:
- Temperature score (range: 0-4)
- Creatinine score (range: 0-4)

See `docs/methodology.md` for detailed scoring algorithms and references.

## Usage Example

```python
# Complete pipeline execution
from src import extract_variables, merge_datasets, calculate_scores, add_patient_info

# Configure paths
config = {
    'base_path': '/path/to/mimic-iv/',
    'cohort_file': 'cohort_definition.xlsx',
    'output_path': 'output/'
}

# Run pipeline
extract_variables.main(config)
merge_datasets.main(config)
calculate_scores.main(config)
add_patient_info.main(config)
```

See `examples/pipeline_example.py` for complete working example.

## Data Privacy and Ethics

This project uses the MIMIC-IV database, which contains de-identified patient data. All analyses comply with:

- MIMIC-IV Data Use Agreement
- PhysioNet Credentialed Health Data License 1.5.0
- HIPAA privacy regulations
- IRB approval for original data collection

**Important:** Do not share raw MIMIC-IV data or results that could re-identify patients.

## Citation

If you use this code in your research, please cite:

```bibtex
@misc{refeeding_mimic2025,
  author = {[PI Name] and Green, James},
  title = {Refeeding Syndrome Identification in ICU Patients Using MIMIC-IV},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/[username]/refeeding-syndrome-mimic}
}
```

**Manuscript Citation** (when published):
[Will be updated upon publication in Journal of Parenteral and Enteral Nutrition]

## MIMIC-IV Citation

```bibtex
@article{mimiciv,
  author = {Johnson, Alistair and Bulgarelli, Lucas and Pollard, Tom and 
            Horng, Steven and Celi, Leo Anthony and Mark, Roger},
  title = {{MIMIC-IV} (version 2.0)},
  journal = {PhysioNet},
  year = {2022},
  doi = {10.13026/7vcr-e114}
}
```

## Contributing

This repository contains research code for a specific study. For questions or issues:
- Open an issue on GitHub
- Contact: jg1984@shp.rutgers.edu

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Note: The MIMIC-IV database itself is subject to PhysioNet's Credentialed Health Data License and separate data use agreements.

## Acknowledgments

- MIMIC-IV database developers and maintainers
- PhysioNet team
- [Institution name]
- Doctoral committee members

## Version History

- **v1.0.0** (2025-11-06): Initial public release
  - Complete data processing pipeline
  - SOFA and APACHE II scoring
  - Documentation and examples

---

**Last Updated:** November 2025  
**Corresponding Author:** [PI Name]  
**Programmer:** James Green (jg1984@shp.rutgers.edu)
