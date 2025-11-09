* Encoding: UTF-8.
DO IF (sofa_components_present = 6).
    COMPUTE sofa_total_new = sofa_total.
ELSE IF (sofa_components_present NE 6).
    COMPUTE sofa_total_new = -99.
END IF.
EXECUTE.
