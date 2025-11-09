* Encoding: UTF-8.
SORT CASES BY subject_id (A) icu_intime (A).

IF $CASENUM = 1 subject_id = subject_id.
DO IF $CASENUM = 1.
END IF.
IF LAG(subject_id) <> subject_id first_adm = 1.
EXECUTE.
SELECT IF first_adm = 1.
EXECUTE.
