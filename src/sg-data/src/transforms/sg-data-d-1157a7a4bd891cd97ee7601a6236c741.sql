-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "BasicCertificate_Total" AS basiccertificate_total,
    "BasicCertificate_Males" AS basiccertificate_males,
    "BasicCertificate_Females" AS basiccertificate_females,
    "AdvancedCertificate_Total" AS advancedcertificate_total,
    "AdvancedCertificate_Males" AS advancedcertificate_males,
    "AdvancedCertificate_Females" AS advancedcertificate_females,
    "Diploma_Total" AS diploma_total,
    "Diploma_Males" AS diploma_males,
    "Diploma_Females" AS diploma_females,
    "AdvancedDiploma_Total" AS advanceddiploma_total,
    "AdvancedDiploma_Males" AS advanceddiploma_males,
    "AdvancedDiploma_Females" AS advanceddiploma_females,
    "QualificationFromProfessionalBodies_Total" AS qualificationfromprofessionalbodies_total,
    "QualificationFromProfessionalBodies_Males" AS qualificationfromprofessionalbodies_males,
    "QualificationFromProfessionalBodies_Females" AS qualificationfromprofessionalbodies_females
FROM "sg-data-d-1157a7a4bd891cd97ee7601a6236c741"
