* Encoding: UTF-8.

EXAMINE VARIABLES=age bmi gcs_total_new nutr_initial_icuday pre_pot pre_phos pre_mag post_pot 
    post_phos post_mag pot_percent phos_percent 
    mag_percent
  /PLOT BOXPLOT HISTOGRAM NPPLOT
  /COMPARE GROUPS
  /STATISTICS DESCRIPTIVES EXTREME
  /CINTERVAL 95
  /MISSING PAIRWISE
  /NOTOTAL.
