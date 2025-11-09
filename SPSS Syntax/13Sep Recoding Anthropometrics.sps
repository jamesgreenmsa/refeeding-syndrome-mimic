* Encoding: UTF-8.
*Recalculated height after updating height 

COMPUTE height_m=height_cm / 100.
EXECUTE.

*Recalculated BMI
    
COMPUTE bmi=adm_weight_kg / (height_m * height_m).
EXECUTE.
