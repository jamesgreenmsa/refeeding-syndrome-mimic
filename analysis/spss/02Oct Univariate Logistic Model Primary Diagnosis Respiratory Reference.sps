* Encoding: UTF-8.

LOGISTIC REGRESSION VARIABLES overall_rfs_presence
  /METHOD=ENTER drg_cat_new 
  /CONTRAST (drg_cat_new)=Indicator
  /CLASSPLOT
  /CASEWISE OUTLIER(2)
  /PRINT=GOODFIT CI(95)
  /CRITERIA=PIN(0.05) POUT(0.10) ITERATE(20) CUT(0.5).
