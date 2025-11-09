* Encoding: UTF-8.

DATASET ACTIVATE DataSet1.
SORT CASES BY subject_id hadm_id stay_id age sex height_cm height_m adm_weight_kg adm_weight_lbs 
    bmi gcs_total sofa_components_present sofa_total apache_total apache_aps_components_present 
    first_careunit icu_los icu_intime drg_code drg_cat nutr_support nutr_initial_icuday pre_pot 
    pre_pot_icuday pre_phos pre_phos_icuday pre_mag pre_mag_icuday post_pot post_pot_nutrday post_phos 
    post_phos_nutrday post_mag post_mag_nutrday pot_percent phos_percent mag_percent pot_rfs_cat 
    phos_rfs_cat mag_rfs_cat overall_rfs_severity overall_rfs_presence anemia asthma copd diabetes etoh 
    gi_bleed dialysis hepatitis liver_failure pancreatitis renal_failure seizure smoker malnutrition 
    alcohol cocaine amphetamines other_substance any_substance_use.
DATASET ACTIVATE DataSet3.
SORT CASES BY subject_id hadm_id stay_id age sex height_cm height_m adm_weight_kg adm_weight_lbs 
    bmi gcs_total sofa_components_present sofa_total apache_total apache_aps_components_present 
    first_careunit icu_los icu_intime drg_code drg_cat nutr_support nutr_initial_icuday pre_pot 
    pre_pot_icuday pre_phos pre_phos_icuday pre_mag pre_mag_icuday post_pot post_pot_nutrday post_phos 
    post_phos_nutrday post_mag post_mag_nutrday pot_percent phos_percent mag_percent pot_rfs_cat 
    phos_rfs_cat mag_rfs_cat overall_rfs_severity overall_rfs_presence anemia asthma copd diabetes etoh 
    gi_bleed dialysis hepatitis liver_failure pancreatitis renal_failure seizure smoker malnutrition 
    alcohol cocaine amphetamines other_substance any_substance_use.
DATASET ACTIVATE DataSet1.
MATCH FILES /FILE=*
  /FILE='DataSet3'
  /RENAME (nutr_starttime rfs_score = d0 d1) 
  /BY subject_id hadm_id stay_id age sex height_cm height_m adm_weight_kg adm_weight_lbs bmi 
    gcs_total sofa_components_present sofa_total apache_total apache_aps_components_present 
    first_careunit icu_los icu_intime drg_code drg_cat nutr_support nutr_initial_icuday pre_pot 
    pre_pot_icuday pre_phos pre_phos_icuday pre_mag pre_mag_icuday post_pot post_pot_nutrday post_phos 
    post_phos_nutrday post_mag post_mag_nutrday pot_percent phos_percent mag_percent pot_rfs_cat 
    phos_rfs_cat mag_rfs_cat overall_rfs_severity overall_rfs_presence anemia asthma copd diabetes etoh 
    gi_bleed dialysis hepatitis liver_failure pancreatitis renal_failure seizure smoker malnutrition 
    alcohol cocaine amphetamines other_substance any_substance_use
  /DROP= d0 d1.
EXECUTE.
