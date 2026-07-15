-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "DidNotAcquireVocationalQualification_Total" AS didnotacquirevocationalqualification_total,
    "DidNotAcquireVocationalQualification_Males" AS didnotacquirevocationalqualification_males,
    "DidNotAcquireVocationalQualification_Females" AS didnotacquirevocationalqualification_females,
    "AcquiredVocationalQualification_Total_Total" AS acquiredvocationalqualification_total_total,
    "AcquiredVocationalQualification_Total_Males" AS acquiredvocationalqualification_total_males,
    "AcquiredVocationalQualification_Total_Females" AS acquiredvocationalqualification_total_females,
    "AcquiredVocationalQualification_BasicCertificate_Total" AS acquiredvocationalqualification_basiccertificate_total,
    "AcquiredVocationalQualification_BasicCertificate_Males" AS acquiredvocationalqualification_basiccertificate_males,
    "AcquiredVocationalQualification_BasicCertificate_Females" AS acquiredvocationalqualification_basiccertificate_females,
    "AcquiredVocationalQualification_AdvancedCertificate_Total" AS acquiredvocationalqualification_advancedcertificate_total,
    "AcquiredVocationalQualification_AdvancedCertificate_Males" AS acquiredvocationalqualification_advancedcertificate_males,
    "AcquiredVocationalQualification_AdvancedCertificate_Females" AS acquiredvocationalqualification_advancedcertificate_females,
    "AcquiredVocationalQualification_Diploma_AdvancedDiploma_Total" AS acquiredvocationalqualification_diploma_advanceddiploma_total,
    "AcquiredVocationalQualification_Diploma_AdvancedDiploma_Males" AS acquiredvocationalqualification_diploma_advanceddiploma_males,
    "AcquiredVocationalQualification_Diploma_AdvancedDiploma_Females" AS acquiredvocationalqualification_diploma_advanceddiploma_females
FROM "sg-data-d-cb0481d629bba3a7a7cfd51ec4a8ed82"
