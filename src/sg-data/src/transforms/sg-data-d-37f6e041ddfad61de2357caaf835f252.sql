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
    "Diploma_AdvancedDiploma_Total" AS diploma_advanceddiploma_total,
    "Diploma_AdvancedDiploma_Males" AS diploma_advanceddiploma_males,
    "Diploma_AdvancedDiploma_Females" AS diploma_advanceddiploma_females
FROM "sg-data-d-37f6e041ddfad61de2357caaf835f252"
