* Encoding: UTF-8.

DATASET ACTIVATE DataSet1.
RECODE first_careunit_new (1=2) (2=1) (3=3) (4=4) INTO first_careunit_medicu_ref.
VARIABLE LABELS  first_careunit_medicu_ref 'IV: Type of ICU Unit (Med ICU as Reference)'.
EXECUTE.

LOGISTIC REGRESSION VARIABLES overall_rfs_presence
  /METHOD=ENTER first_careunit_medicu_ref 
  /CONTRAST (first_careunit_medicu_ref)=Indicator(1)
  /CLASSPLOT
  /CASEWISE OUTLIER(2)
  /PRINT=GOODFIT CI(95)
  /CRITERIA=PIN(0.05) POUT(0.10) ITERATE(20) CUT(0.5).
