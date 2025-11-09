* Encoding: UTF-8.
Compute overall_rfs_presence = 0.
IF (overall_rfs_severity = 0)  overall_rfs_presence = 0.
IF (overall_rfs_severity > 0) overall_rfs_presence = 1.
Execute.

***********************************************************************************.
* Added by Dr. Samavat.
DATASET ACTIVATE DataSet1.
RECODE overall_rfs_severity (0=0) (1=1) (2=1) (3=1) INTO RFS_DV_dich.
EXECUTE.

MISSING VALUES RFS_DV_dich (-99).
VALUE LABELS RFS_DV_dich
  0 'Absent'
  1 'Present'
  -99 'Missing'.
EXECUTE.

FREQUENCIES VARIABLES=RFS_DV_dich
  /ORDER=ANALYSIS.
***********************************************************************************.
