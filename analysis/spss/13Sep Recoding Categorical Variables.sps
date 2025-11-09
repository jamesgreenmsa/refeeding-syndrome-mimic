* Encoding: UTF-8.
*Recoding ICU Units

RECODE first_careunit (1=1) (2=1) (3=2) (4=3) (5=4) (6=4) (7=4) INTO first_careunit_new.
VARIABLE LABELS  first_careunit_new 'Type of ICU Unit'.
EXECUTE.

*Recoding GI PMH
    
COMPUTE gastro = 0.
IF (gi_bleed = 1) gastro = 1.
IF (hepatitis = 1) gastro = 1.
IF (liver_failure = 1) gastro = 1.
IF (pancreatitis = 1) gastro = 1.
EXECUTE.

*Recoding Renal Failure
    
COMPUTE renal_failure_new = 0.
IF (dialysis = 1) renal_failure_new = 1.
IF (renal_failure = 1) renal_failure_new = 1.
EXECUTE.
    
*Recoding DRG Categories

RECODE drg_cat (1=1) (3=1) (5=1) (6=1) (9=1) (10=1) (13=1) (15=1) (16=1) (18=1) (2=2) (4=3) (7=4) 
    (8=4) (11=5) (14=5) (19=5) (12=6) (17=7) (-99=-99) INTO drg_cat_new.
VARIABLE LABELS  drg_cat_new 'Condensed DRG Categories'.
EXECUTE.

* Recoding Alcohol and Recreational Drug Use
    
COMPUTE alcohol_adm = 0.
IF (alcohol = 1) alcohol_adm = 1.
IF (etoh_charted = 1) alcohol_adm =1.
EXECUTE.

COMPUTE recreational_drug_adm = 0.
IF (recreational_drug = 1) recreational_drug_adm = 1.
IF (recreational_drug_charted = 1) recreational_drug_adm = 1.
EXECUTE.
