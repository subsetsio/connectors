-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "NoVocationalQualification_Total" AS novocationalqualification_total,
    "NoVocationalQualification_Males" AS novocationalqualification_males,
    "NoVocationalQualification_Females" AS novocationalqualification_females,
    "AcquiredVocationalQualification_Total_Total" AS acquiredvocationalqualification_total_total,
    "AcquiredVocationalQualification_Total_Males" AS acquiredvocationalqualification_total_males,
    "AcquiredVocationalQualification_Total_Females" AS acquiredvocationalqualification_total_females,
    "AcquiredVocationalQualification_BasicCertificate_Total" AS acquiredvocationalqualification_basiccertificate_total,
    "AcquiredVocationalQualification_BasicCertificate_Males" AS acquiredvocationalqualification_basiccertificate_males,
    "AcquiredVocationalQualification_BasicCertificate_Females" AS acquiredvocationalqualification_basiccertificate_females,
    "AcquiredVocationalQualification_AdvancedCertificate_Total" AS acquiredvocationalqualification_advancedcertificate_total,
    "AcquiredVocationalQualification_AdvancedCertificate_Males" AS acquiredvocationalqualification_advancedcertificate_males,
    "AcquiredVocationalQualification_AdvancedCertificate_Females" AS acquiredvocationalqualification_advancedcertificate_females,
    "AcquiredVocationalQualification_Diploma_Total" AS acquiredvocationalqualification_diploma_total,
    "AcquiredVocationalQualification_Diploma_Males" AS acquiredvocationalqualification_diploma_males,
    "AcquiredVocationalQualification_Diploma_Females" AS acquiredvocationalqualification_diploma_females,
    "AcquiredVocationalQualification_AdvancedDiploma_Total" AS acquiredvocationalqualification_advanceddiploma_total,
    "AcquiredVocationalQualification_AdvancedDiploma_Males" AS acquiredvocationalqualification_advanceddiploma_males,
    "AcquiredVocationalQualification_AdvancedDiploma_Females" AS acquiredvocationalqualification_advanceddiploma_females,
    "AcquiredVocationalQualification_QualificationFromProfessionalBo" AS acquiredvocationalqualification_qualificationfromprofessionalbo,
    "AcquiredVocationalQualification_QualificationFromProfessionalBo_1" AS acquiredvocationalqualification_qualificationfromprofessionalbo_1,
    "AcquiredVocationalQualification_QualificationFromProfessionalBo_2" AS acquiredvocationalqualification_qualificationfromprofessionalbo_2
FROM "sg-data-d-1f0ae6f20f97689100cdfaae44b18431"
