-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Field of doctorate" AS field_of_doctorate,
    "Female doctorate recipients" AS female_doctorate_recipients,
    "Doctorate recipients with definite commitments" AS doctorate_recipients_with_definite_commitments,
    "Location of definite commitments - United States - Total" AS location_of_definite_commitments_united_states_total,
    "Location of definite commitments - United States - Postdoctoral study" AS location_of_definite_commitments_united_states_postdoctoral_study,
    "Location of definite commitments - United States - Academic employment" AS location_of_definite_commitments_united_states_academic_employment,
    "Location of definite commitments - United States - Industry employmenta" AS location_of_definite_commitments_united_states_industry_employmenta,
    "Location of definite commitments - United States - Otherb" AS location_of_definite_commitments_united_states_otherb,
    "Location of definite commitments - Abroad - Otherb" AS location_of_definite_commitments_abroad_otherb,
    "Location of definite commitments - Unknown - Otherb" AS location_of_definite_commitments_unknown_otherb
FROM "ncses-nsf25349-tab006-004"
