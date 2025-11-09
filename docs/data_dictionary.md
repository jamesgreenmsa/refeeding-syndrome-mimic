# Data Dictionary

## Overview
This document describes all variables in the analytical dataset for the refeeding syndrome study using MIMIC-IV data.

## Patient Identifiers

| Variable | Type | Description | Source |
|----------|------|-------------|--------|
| `subject_id` | String | Unique patient identifier | MIMIC-IV |
| `hadm_id` | String | Hospital admission identifier | MIMIC-IV |
| `stay_id` | String | ICU stay identifier | MIMIC-IV |

## Severity Scores

### SOFA Score (Sequential Organ Failure Assessment)

| Variable | Type | Range | Description |
|----------|------|-------|-------------|
| `sofa_score` | Integer | 0-24 | Total SOFA score (sum of six organ system scores) |
| `sofa_platelet` | Integer | 0-4 | Coagulation component |
| `sofa_bilirubin` | Integer | 0-4 | Liver component |
| `sofa_creatinine` | Integer | 0-4 | Renal component |
| `sofa_gcs` | Integer | 0-4 | Neurological component (based on GCS) |
| `sofa_pf` | Integer | 0-4 | Respiratory component (PaO₂/FiO₂ ratio) |
| `sofa_cardio_score` | Integer | 0-4 | Cardiovascular component |

**SOFA Scoring Criteria:**

**Coagulation (Platelets ×10³/μL):**
- 0: ≥150
- 1: <150
- 2: <100
- 3: <50
- 4: <20

**Liver (Bilirubin mg/dL):**
- 0: <1.2
- 1: 1.2-1.9
- 2: 2.0-5.9
- 3: 6.0-11.9
- 4: ≥12.0

**Renal (Creatinine mg/dL):**
- 0: <1.2
- 1: 1.2-1.9
- 2: 2.0-3.4
- 3: 3.5-4.9
- 4: ≥5.0

**Neurological (GCS total):**
- 0: 15
- 1: 13-14
- 2: 10-12
- 3: 6-9
- 4: <6

**Respiratory (PaO₂/FiO₂ mmHg):**
- 0: ≥400
- 1: 300-399
- 2: 200-299
- 3: 100-199 (with ventilation)
- 4: <100 (with ventilation)

**Reference:** Vincent JL, et al. Intensive Care Med. 1996;22(7):707-710.

### APACHE II Score (Simplified)

| Variable | Type | Range | Description |
|----------|------|-------|-------------|
| `apache_score` | Integer | 0-8 | Simplified APACHE II score (partial components) |
| `apache_creatinine` | Integer | 0-4 | Creatinine component |
| `apache_temp` | Integer | 0-4 | Temperature component |

**Note:** This is a simplified APACHE II implementation using only components readily available in the dataset.

**APACHE II Temperature Scoring (°C):**
- 4: ≥41 or ≤29.9
- 3: 39-40.9 or 30-31.9
- 2: 38.5-38.9 or 32-33.9
- 1: 34-35.9
- 0: 36-38.4

**APACHE II Creatinine Scoring (mg/dL):**
- 4: ≥3.5
- 3: 2.0-3.4
- 2: 1.5-1.9 or <0.6
- 0: 0.6-1.4

**Reference:** Knaus WA, et al. Crit Care Med. 1985;13(10):818-829.

## Laboratory Values

All laboratory values represent the first measurement within 24 hours of ICU admission.

| Variable | Type | Units | Normal Range | MIMIC-IV itemid |
|----------|------|-------|--------------|-----------------|
| `platelet` | Float | ×10³/μL | 150-400 | 51265 |
| `bilirubin` | Float | mg/dL | 0.1-1.2 | 50885 |
| `creatinine` | Float | mg/dL | 0.7-1.3 | 50912 |
| `pao2` | Float | mmHg | 75-100 | 50821 |

### Optional Electrolytes (if implemented)

| Variable | Type | Units | Normal Range | MIMIC-IV itemid |
|----------|------|-------|--------------|-----------------|
| `sodium` | Float | mEq/L | 136-145 | 50983 |
| `potassium` | Float | mEq/L | 3.5-5.0 | 50971 |
| `phosphate` | Float | mg/dL | 2.5-4.5 | 50970 |
| `magnesium` | Float | mg/dL | 1.7-2.2 | 50960 |

## Vital Signs and Assessments

All measurements represent the first value within 24 hours of ICU admission.

| Variable | Type | Units | Normal Range | MIMIC-IV itemid |
|----------|------|-------|--------------|-----------------|
| `temperature` | Float | °C | 36.5-37.5 | 223761 |
| `map` | Float | mmHg | 70-100 | 220052 |
| `fio2` | Float | % | 21-100 | 223835, 3420 |

### Glasgow Coma Scale (GCS)

| Variable | Type | Range | Description | MIMIC-IV itemid |
|----------|------|-------|-------------|-----------------|
| `gcs_eye` | Integer | 1-4 | Eye opening response | 220739 |
| `gcs_motor` | Integer | 1-6 | Motor response | 223901 |
| `gcs_verbal` | Integer | 1-5 | Verbal response | 223900 |
| `gcs_total` | Integer | 3-15 | Total GCS (sum of components) | Calculated |

**GCS Interpretation:**
- 14-15: Mild impairment
- 9-13: Moderate impairment
- 3-8: Severe impairment

## Calculated Variables

| Variable | Type | Units | Description | Calculation |
|----------|------|-------|-------------|-------------|
| `fio2_fraction` | Float | Decimal | FiO₂ as fraction | `fio2 / 100` |
| `pf_ratio` | Float | mmHg | PaO₂/FiO₂ ratio | `pao2 / fio2_fraction` |

**PaO₂/FiO₂ Ratio Interpretation:**
- >400: Normal
- 300-400: Mild acute lung injury
- 200-300: Moderate acute lung injury  
- <200: Severe acute lung injury (ARDS)

## Medical History Variables

Binary indicators (0/1 or Yes/No) for chronic conditions and substance use history.

| Variable | Type | Description |
|----------|------|-------------|
| `ANEMIA` | Binary | History of anemia |
| `ASTHMA` | Binary | History of asthma |
| `COPD` | Binary | Chronic obstructive pulmonary disease |
| `DIABETES - INSULIN` | Binary | Diabetes mellitus requiring insulin |
| `DIABETES - ORAL AGENT` | Binary | Diabetes mellitus managed with oral agents |
| `ETOH` | Binary | History of alcohol use |
| `GI BLEED` | Binary | History of gastrointestinal bleeding |
| `HEMO OR PD` | Binary | History of hemodialysis or peritoneal dialysis |
| `HEPATITIS` | Binary | History of hepatitis |
| `LIVER FAILURE` | Binary | History of liver failure |
| `PANCREATITIS` | Binary | History of pancreatitis |
| `RENAL FAILURE` | Binary | History of renal failure |
| `SEIZURES` | Binary | History of seizures |
| `SMOKER` | Binary | Current or former smoker |

## Data Quality Notes

### Missing Data
- Laboratory values may be missing if not ordered within the 24-hour window
- GCS components may be missing if patient is sedated or intubated
- Missing values are represented as `NaN` or empty cells

### Data Collection Window
- All clinical measurements are from the **first 24 hours** of ICU admission
- Timing is calculated from `icustays.intime` (ICU admission time)

### Measurement Selection
- When multiple measurements exist within the 24-hour window, the **first** measurement is used
- This approach captures the patient's status at ICU admission

### Scoring Defaults
- When a clinical measurement is missing, the corresponding score component defaults to 0
- This conservative approach may underestimate severity in some cases

## Data Sources

### Primary MIMIC-IV Tables Used
1. **icustays.csv**: ICU stay information and timing
2. **labevents.csv**: Laboratory measurements
3. **chartevents.csv**: Vital signs and clinical assessments
4. **patients.csv**: Demographics (if included)
5. **admissions.csv**: Hospital admission details (if included)

### Cohort Definition
The study cohort is defined in an external Excel file containing:
- Inclusion/exclusion criteria applications
- Final list of eligible ICU stays
- Additional patient characteristics

## Variable Naming Conventions

- **IDs**: Lowercase with underscores (e.g., `subject_id`, `stay_id`)
- **Scores**: Prefix with score type (e.g., `sofa_`, `apache_`)
- **Components**: Score name + organ system (e.g., `sofa_platelet`)
- **Raw values**: Lowercase measurement name (e.g., `creatinine`, `temperature`)
- **Medical history**: ALL CAPS with spaces (e.g., `DIABETES - INSULIN`)

## Units and Conversions

All values are reported in the units specified above. No unit conversions are applied unless explicitly noted.

**Temperature:** All temperatures are in Celsius (°C)
**Pressure:** All pressures are in millimeters of mercury (mmHg)
**Laboratory values:** Use standard US units (mg/dL, mEq/L, etc.)

## References

1. Vincent JL, et al. The SOFA (Sepsis-related Organ Failure Assessment) score to describe organ dysfunction/failure. Intensive Care Med. 1996;22(7):707-710.

2. Knaus WA, et al. APACHE II: a severity of disease classification system. Crit Care Med. 1985;13(10):818-829.

3. Johnson A, et al. MIMIC-IV (version 2.0). PhysioNet. 2022. DOI: 10.13026/7vcr-e114

## Version History

- **v1.0** (2025-11-06): Initial documentation for public release

---

**Last Updated:** November 6, 2025  
**Contact:** James Green (jg1984@shp.rutgers.edu)
