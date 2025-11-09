* Encoding: UTF-8.

DATASET ACTIVATE DataSet1.
EXAMINE VARIABLES=age_new bmi gcs_total_new sofa_total_new icu_los nutr_initial_icuday pre_pot 
    pre_phos pre_mag post_pot post_phos post_mag
  /PLOT BOXPLOT HISTOGRAM NPPLOT
  /COMPARE GROUPS
  /PERCENTILES(25,50,75) HAVERAGE
  /STATISTICS DESCRIPTIVES EXTREME
  /CINTERVAL 95
  /MISSING PAIRWISE
  /NOTOTAL.
