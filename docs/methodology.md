# Methodology

## Study Overview

This analysis examines refeeding syndrome in critically ill patients using the MIMIC-IV database. The goal is to identify clinical predictors and outcomes associated with refeeding syndrome in ICU settings.

## Data Source

### MIMIC-IV Database
- **Version:** 2.0 or higher
- **Institution:** Beth Israel Deaconess Medical Center, Boston, MA
- **Time Period:** 2008-2019
- **Database Type:** De-identified electronic health records
- **Access:** Requires PhysioNet credentialing and CITI training

**Citation:** Johnson A, Bulgarelli L, Pollard T, Horng S, Celi LA, Mark R. MIMIC-IV (version 2.0). PhysioNet. 2022. DOI: 10.13026/7vcr-e114

## Study Population

### Inclusion Criteria
[To be specified based on your cohort definition]
- Adult ICU patients (≥18 years)
- ICU length of stay ≥24 hours
- [Additional criteria from your cohort definition file]

### Exclusion Criteria
[To be specified based on your cohort definition]
- [Specific exclusion criteria]

### Cohort Definition
The study cohort is defined in `cohort_definition.xlsx`, which contains:
- Subject, hospital admission, and ICU stay identifiers
- Inclusion/exclusion status
- Additional cohort-specific variables

## Data Extraction Methodology

### Temporal Window
- **Primary window:** First 24 hours of ICU admission
- **Rationale:** Captures acute physiology at ICU entry while minimizing temporal confounding
- **Reference time:** ICU admission time (`icustays.intime`)

### Variable Selection Strategy

#### 1. Laboratory Values
Extracted from `labevents.csv` using MIMIC-IV itemid mappings:
- Platelet count (itemid: 51265)
- Total bilirubin (itemid: 50885)
- Serum creatinine (itemid: 50912)
- Partial pressure of oxygen - PaO₂ (itemid: 50821)

**Selection logic:**
- Include measurements between ICU admission and 24 hours post-admission
- If multiple values exist, select the **first** measurement
- Missing values handled as described in Data Quality section

#### 2. Vital Signs and Clinical Assessments
Extracted from `chartevents.csv`:
- Temperature (itemid: 223761)
- Mean arterial pressure (itemid: 220052)
- Fraction of inspired oxygen - FiO₂ (itemids: 223835, 3420)
- Glasgow Coma Scale components (itemids: 220739, 223900, 223901)

**Selection logic:**
- Same temporal window as laboratory values
- First measurement within 24-hour window selected
- GCS total calculated as sum of eye, motor, and verbal components

### Data Processing Pipeline

#### Step 1: Variable Extraction (`01_extract_variables.py`)
```
Input: Raw MIMIC-IV tables (labevents.csv, chartevents.csv, icustays.csv)
Processing:
  1. Load cohort definition
  2. For each patient:
     a. Identify ICU admission time
     b. Extract measurements within 24-hour window
     c. Select first measurement per variable
  3. Save individual variable files (feather format)
Output: Separate files for each clinical variable
```

**Technical approach:**
- Chunk-based processing to handle large files (default: 100,000 rows/chunk)
- Feather format for efficient storage and retrieval
- Memory-efficient streaming prevents system overload

#### Step 2: Dataset Merging (`02_merge_datasets.py`)
```
Input: Individual variable files from Step 1
Processing:
  1. Initialize base dataset with cohort stay_ids
  2. Sequentially merge each variable file on stay_id
  3. Handle missing data (left join preserves all stays)
Output: progressive_merge.csv (combined dataset)
```

**Technical approach:**
- Progressive chunked merging
- Preserves all cohort members (left join strategy)
- One measurement per stay per variable

#### Step 3: Score Calculation (`03_calculate_scores.py`)
```
Input: Combined dataset from Step 2
Processing:
  1. Calculate derived variables (GCS total, PaO₂/FiO₂ ratio)
  2. Apply SOFA scoring criteria to each component
  3. Apply APACHE II scoring criteria (simplified)
  4. Sum components for total scores
  5. Merge with medical history
Output: sofa_apache_scores.csv
```

#### Step 4: Add Patient Information (`05_add_patient_info.py`)
```
Input: Scores dataset + cohort definition file
Processing:
  1. Merge patient demographics
  2. Add admission details
  3. Include additional clinical characteristics
Output: sofa_apache_full_with_info.csv (final analytical dataset)
```

## Scoring Methodology

### SOFA Score (Sequential Organ Failure Assessment)

**Purpose:** Evaluate organ dysfunction in critically ill patients

**Components:** Six organ systems scored 0-4 each
1. **Respiration:** PaO₂/FiO₂ ratio
2. **Coagulation:** Platelet count
3. **Liver:** Bilirubin level
4. **Cardiovascular:** Mean arterial pressure and vasopressor use
5. **Neurological:** Glasgow Coma Scale
6. **Renal:** Creatinine level

**Total Range:** 0-24 (higher = more severe dysfunction)

**Implementation notes:**
- Cardiovascular component simplified (detailed vasopressor dosing not always available)
- Missing components default to 0 (may underestimate severity)

**Reference:** Vincent JL, et al. Intensive Care Med. 1996;22(7):707-710.

### APACHE II Score (Simplified)

**Purpose:** Predict ICU mortality risk

**Standard components:** 12 physiologic variables + age + chronic health

**Our implementation:** Simplified version using available variables
- Temperature (0-4 points)
- Creatinine (0-4 points)
- [Additional components as implemented]

**Note:** This is a partial APACHE II score using readily available MIMIC-IV data. Not intended for clinical mortality prediction; used for characterizing cohort severity.

**Reference:** Knaus WA, et al. Crit Care Med. 1985;13(10):818-829.

## Data Quality and Limitations

### Missing Data Handling

**Laboratory values:**
- Not all patients have all tests ordered
- Tests may be ordered outside the 24-hour window
- Strategy: Keep missing values as `NaN`; scoring components default to 0

**Vital signs:**
- More complete than laboratory data
- Continuous monitoring provides multiple measurements
- Strategy: First value within window selected

**GCS components:**
- May be missing if patient sedated/intubated
- Verbal component often unobtainable in intubated patients
- Strategy: Calculate total GCS from available components (min_count=1)

### Known Limitations

1. **Temporal selection bias:**
   - First measurement may not represent peak severity
   - Alternative: Could use worst value, but introduces different bias

2. **SOFA cardiovascular component:**
   - Detailed vasopressor dosing not always available
   - Simplified scoring may underestimate cardiovascular dysfunction

3. **APACHE II incompleteness:**
   - Partial score only; not comparable to full APACHE II
   - Should not be used for mortality prediction
   - Useful for cohort characterization only

4. **Measurement timing:**
   - Tests ordered at clinician discretion (not standardized protocol)
   - Sicker patients may have more frequent testing
   - Creates potential selection bias

5. **Refeeding syndrome identification:**
   - [Specific methodology to be added based on study protocol]
   - Electrolyte monitoring patterns
   - Clinical criteria application

## Statistical Analysis Plan

[This section should be customized for your specific study]

### Primary Outcomes
- [Define primary outcomes]

### Secondary Outcomes
- [Define secondary outcomes]

### Statistical Methods
- Descriptive statistics for cohort characterization
- [Additional methods as appropriate]

### Subgroup Analyses
- [Define any planned subgroup analyses]

## Reproducibility

### Software Environment
```
Python 3.8+
pandas 1.3.0+
numpy 1.21.0+
openpyxl 3.0.0+
pyarrow 5.0.0+
```

### Random Seeds
- Sample creation: seed = 42
- All random processes documented with seeds for reproducibility

### Version Control
- Code hosted on GitHub: [repository URL]
- Release version: v1.0.0
- DOI: [to be added after publication]

## Ethical Considerations

### Data Use Agreement
This study complies with the MIMIC-IV Data Use Agreement:
- Data used only for research purposes
- No attempts to re-identify patients
- Appropriate citation of MIMIC-IV database
- Public code sharing (this repository)

### IRB Approval
- MIMIC-IV data collection approved by Institutional Review Boards of MIT and Beth Israel Deaconess Medical Center
- Informed consent waived (de-identified retrospective data)

### Privacy Protection
- All patient identifiers removed by MIMIC-IV creators
- Dates shifted randomly per patient
- No protected health information (PHI) in analytical dataset
- No geographic information beyond hospital location

## Code Availability

All analysis code is publicly available to ensure transparency and reproducibility:
- **Repository:** [GitHub URL]
- **License:** MIT
- **Citation:** [To be added]

As required by MIMIC-IV Data Use Agreement, this code sharing enables:
- Method verification
- Study reproduction
- Extension by other researchers
- Scientific transparency

## Manuscript Methods Section Template

Below is suggested text for the Methods section of a manuscript:

---

**Data Source and Study Population**

We conducted a retrospective cohort study using the Medical Information Mart for Intensive Care (MIMIC-IV) database version 2.0, which contains de-identified electronic health records from Beth Israel Deaconess Medical Center (2008-2019).¹ [Describe inclusion/exclusion criteria]. The final cohort included [N] ICU stays.

**Data Extraction**

Clinical variables were extracted from the first 24 hours of ICU admission to capture acute physiology while minimizing temporal confounding. Laboratory values (platelets, bilirubin, creatinine, PaO₂) and vital signs (temperature, mean arterial pressure, FiO₂, Glasgow Coma Scale) were obtained from the labevents and chartevents tables, respectively. When multiple measurements existed within the 24-hour window, the first value was selected.

**Severity of Illness Assessment**

We calculated the Sequential Organ Failure Assessment (SOFA) score² to evaluate organ dysfunction, scoring six organ systems (respiration, coagulation, liver, cardiovascular, neurological, renal) from 0-4 each (total range 0-24, higher indicating greater dysfunction). A simplified Acute Physiology and Chronic Health Evaluation (APACHE II) score³ was calculated using available physiologic variables for cohort characterization.

**Refeeding Syndrome Identification**

[Add your specific refeeding syndrome definition and identification methodology]

**Statistical Analysis**

[Add your specific statistical methods]

**Code Availability**

All data processing and analysis code is publicly available at [GitHub URL] to ensure transparency and reproducibility.

---

## References

1. Johnson A, Bulgarelli L, Pollard T, Horng S, Celi LA, Mark R. MIMIC-IV (version 2.0). PhysioNet. 2022. DOI: 10.13026/7vcr-e114

2. Vincent JL, Moreno R, Takala J, et al. The SOFA (Sepsis-related Organ Failure Assessment) score to describe organ dysfunction/failure. Intensive Care Med. 1996;22(7):707-710.

3. Knaus WA, Draper EA, Wagner DP, Zimmerman JE. APACHE II: a severity of disease classification system. Crit Care Med. 1985;13(10):818-829.

---

**Document Version:** 1.0  
**Last Updated:** November 6, 2025  
**Contact:** James Green (jg1984@shp.rutgers.edu)
