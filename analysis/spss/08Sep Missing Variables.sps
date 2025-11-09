* Encoding: UTF-8.
RECODE height_cm (MISSING=-99).
MISSING VALUES height_cm (-99).
VALUE LABELS height_cm
-99 'Missing'.
EXECUTE.

RECODE height_m (MISSING=-99).
MISSING VALUES height_m (-99).
VALUE LABELS height_m
-99 'Missing'.
EXECUTE.

RECODE adm_weight_lbs (MISSING=-99).
MISSING VALUES adm_weight_lbs (-99).
VALUE LABELS adm_weight_lbs
-99 'Missing'.
EXECUTE.

RECODE bmi (MISSING=-99).
MISSING VALUES bmi (-99).
VALUE LABELS bmi
-99 'Missing'.
EXECUTE.

RECODE gcs_total (MISSING=-99).
MISSING VALUES gcs_total (-99).
VALUE LABELS gcs_total
-99 'Missing'.
EXECUTE.

RECODE drg_code (MISSING=-99).
MISSING VALUES drg_code (-99).
VALUE LABELS drg_code
-99 'Missing'.
EXECUTE.

RECODE drg_cat (MISSING=-99).
MISSING VALUES drg_cat (-99).
VALUE LABELS drg_cat
-99 'Missing'.
EXECUTE.
