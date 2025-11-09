* Encoding: UTF-8.

COMPUTE gcs_total_new=gcs_eye + gcs_verbal + gcs_motor.
EXECUTE.

RECODE gcs_eye (MISSING=-99).
MISSING VALUES gcs_eye (-99).
VALUE LABELS gcs_eye
-99 'Missing'.
EXECUTE.

RECODE gcs_verbal (MISSING=-99).
MISSING VALUES gcs_verbal (-99).
VALUE LABELS gcs_verbal
-99 'Missing'.
EXECUTE.

RECODE gcs_motor (MISSING=-99).
MISSING VALUES gcs_motor (-99).
VALUE LABELS gcs_motor
-99 'Missing'.
EXECUTE.

RECODE gcs_total_new (MISSING=-99).
MISSING VALUES gcs_total_new (-99).
VALUE LABELS gcs_total_new
-99 'Missing'.
EXECUTE.
