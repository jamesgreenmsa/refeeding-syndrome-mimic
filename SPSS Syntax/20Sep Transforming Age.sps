* Encoding: UTF-8.
DO IF (age = 91).
    COMPUTE age_new = -99.
ELSE IF (age NE 91).
    COMPUTE age_new = age.
END IF.
EXECUTE.
