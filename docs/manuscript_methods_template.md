# Methods Section Text for Manuscript

## For Journal of Parenteral and Enteral Nutrition

This document provides ready-to-use text for the Methods section and Data Availability statement that can be directly incorporated into your manuscript.

---

## METHODS SECTION

### Data Source and Study Population

We conducted a retrospective cohort study using the Medical Information Mart for Intensive Care IV (MIMIC-IV) database version 2.0, a publicly available critical care database containing de-identified electronic health records from Beth Israel Deaconess Medical Center spanning 2008-2019.¹ The database includes comprehensive clinical data for over 300,000 hospital admissions and 70,000 intensive care unit (ICU) stays. [Add your specific inclusion/exclusion criteria here]. The final analytic cohort included [N] ICU stays from [N] unique patients.

### Clinical Variable Extraction

Clinical variables were extracted from the first 24 hours of ICU admission to capture acute physiology and minimize temporal confounding. Laboratory measurements including platelet count (itemid 51265), total bilirubin (50885), serum creatinine (50912), and partial pressure of arterial oxygen (50821) were obtained from the labevents table. Vital signs and clinical assessments including temperature (223761), mean arterial pressure (220052), fraction of inspired oxygen (223835, 3420), and Glasgow Coma Scale components (220739, 223900, 223901) were extracted from the chartevents table. When multiple measurements existed within the 24-hour window, the first recorded value was selected to represent admission physiology. Data processing was performed using Python 3.9 with pandas 1.3.0.

### Severity of Illness Assessment

We calculated the Sequential Organ Failure Assessment (SOFA) score² to quantify organ dysfunction across six physiologic systems: respiration (PaO₂/FiO₂ ratio), coagulation (platelet count), liver (bilirubin), cardiovascular (mean arterial pressure and vasopressor use), neurological (Glasgow Coma Scale), and renal (creatinine). Each component was scored from 0 (normal) to 4 (severe dysfunction) based on established thresholds, with total scores ranging from 0 to 24. Higher scores indicate greater severity of organ dysfunction. A simplified Acute Physiology and Chronic Health Evaluation II (APACHE II)³ score was calculated using available physiologic variables (temperature, creatinine) for cohort characterization purposes.

### [Add your refeeding syndrome methodology here]

### Statistical Analysis

[Add your specific statistical methods]

Descriptive statistics were calculated for demographic and clinical variables. [Continue with your analytic approach]. All statistical analyses were performed using [software], with statistical significance defined as a two-tailed p-value <0.05.

---

## DATA AVAILABILITY STATEMENT

### Option 1 (Detailed):

The MIMIC-IV database is publicly available to qualified researchers who complete required human subjects research training and agree to a data use agreement (available at https://physionet.org/content/mimiciv/). All data processing and analysis code used in this study is publicly available at [GitHub URL] under an MIT license to ensure transparency and reproducibility. The code repository includes detailed documentation of data extraction procedures, variable definitions with MIMIC-IV itemid mappings, scoring algorithms, and complete analytical pipeline. Raw MIMIC-IV data cannot be shared directly per data use agreement terms, but interested researchers can obtain independent access through PhysioNet.

### Option 2 (Concise):

The MIMIC-IV database is publicly available through PhysioNet (https://physionet.org/content/mimiciv/) to credentialed researchers. All analysis code is available at [GitHub URL] to ensure reproducibility and transparency.

---

## CODE AVAILABILITY STATEMENT (if separate section required)

All source code for data extraction, processing, and analysis is publicly available at [GitHub URL] under an MIT license. The repository includes:
- Python scripts for clinical variable extraction from MIMIC-IV
- SOFA and APACHE II score calculation algorithms  
- Complete data processing pipeline documentation
- Variable definitions with MIMIC-IV itemid mappings
- Instructions for reproducing the analysis

---

## SUPPLEMENTARY MATERIAL TEXT (if applicable)

Supplementary materials include:
- Data Dictionary: Complete definitions of all variables including MIMIC-IV source tables and itemid mappings
- Methodology Documentation: Detailed description of data extraction, processing, and scoring procedures
- MIMIC-IV Setup Guide: Instructions for obtaining database access and configuring the analysis environment

Available at: [GitHub URL]/docs/

---

## ACKNOWLEDGMENTS SECTION

We acknowledge the MIMIC-IV database developers and the patients whose de-identified data contributed to this research. We thank the PhysioNet team for maintaining public access to critical care research databases.

---

## REFERENCES TO ADD

1. Johnson A, Bulgarelli L, Pollard T, Horng S, Celi LA, Mark R. MIMIC-IV (version 2.0). PhysioNet. 2022. doi:10.13026/7vcr-e114

2. Vincent JL, Moreno R, Takala J, et al. The SOFA (Sepsis-related Organ Failure Assessment) score to describe organ dysfunction/failure. Intensive Care Med. 1996;22(7):707-710.

3. Knaus WA, Draper EA, Wagner DP, Zimmerman JE. APACHE II: a severity of disease classification system. Crit Care Med. 1985;13(10):818-829.

---

## WORD COUNT TIPS FOR JPEN

The Journal of Parenteral and Enteral Nutrition prefers manuscripts under 3000 words. To fit this constraint:

**Methods section** (~600-800 words total):
- Data Source: 100-150 words
- Variable Extraction: 150-200 words  
- Severity Assessment: 100-150 words
- [Your refeeding methodology]: 150-250 words
- Statistical Analysis: 100-150 words

**Data Availability** (~50-100 words):
- Use concise version if word count is tight
- Can reference supplementary materials for details

**Code citation in text:**
- Mention once in Methods: "All analysis code is publicly available (https://github.com/[username]/refeeding-syndrome-mimic)"
- Full details in Data Availability statement

---

## CUSTOMIZATION CHECKLIST

Before submission, update the following:
- [ ] Replace [GitHub URL] with actual repository URL
- [ ] Replace [N] with actual sample sizes
- [ ] Add specific inclusion/exclusion criteria
- [ ] Add refeeding syndrome definition and methodology
- [ ] Add complete statistical analysis plan
- [ ] Add software/package versions used for analysis
- [ ] Add funding acknowledgments if applicable
- [ ] Add IRB/ethics approval statement if required
- [ ] Replace [PI Name] in citations and acknowledgments
- [ ] Verify all MIMIC-IV itemid numbers are correct
- [ ] Confirm journal-specific formatting requirements

---

**Document Created:** November 6, 2025  
**For Manuscript:** [Title]  
**Primary Author:** [PI Name]  
**Programmer:** James Green
