* Encoding: UTF-8.

LOGISTIC REGRESSION VARIABLES overall_rfs_presence
  /METHOD=ENTER age_new bmi sofa_total_new first_careunit_medicu_ref nutr_initial_icuday diabetes 
    etoh 
  /CONTRAST (first_careunit_medicu_ref)=Indicator(1)
  /CONTRAST (diabetes)=Indicator(1)
  /CONTRAST (etoh)=Indicator(1)
  /CLASSPLOT
  /CASEWISE OUTLIER(2)
  /PRINT=GOODFIT CI(95)
  /CRITERIA=PIN(0.05) POUT(0.10) ITERATE(20) CUT(0.5).
