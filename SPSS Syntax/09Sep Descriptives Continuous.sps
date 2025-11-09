* Encoding: UTF-8.

EXAMINE VARIABLES=age bmi gcs_total sofa_components_present sofa_total apache_total 
    apache_aps_components_present icu_los pre_pot pre_phos pre_mag nutr_initial_icuday post_pot 
    post_pot_nutrday post_phos post_phos_nutrday post_mag post_mag_nutrday pot_percent phos_percent 
    mag_percent
  /ID=subject_id
  /PLOT BOXPLOT HISTOGRAM NPPLOT
  /COMPARE GROUPS
  /STATISTICS DESCRIPTIVES EXTREME
  /CINTERVAL 95
  /MISSING PAIRWISE
  /NOTOTAL.
