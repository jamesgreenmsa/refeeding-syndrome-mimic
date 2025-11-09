* Encoding: UTF-8.

DATASET ACTIVATE DataSet1.
FREQUENCIES VARIABLES=sex first_careunit_new drg_cat_new nutr_support overall_rfs_severity 
    overall_rfs_presence copd diabetes etoh gastro renal_failure_new malnutrition alcohol_adm 
    recreational_drug_adm
  /ORDER=ANALYSIS.
