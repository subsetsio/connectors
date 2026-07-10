-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("time_period" AS BIGINT) AS time_period,
    "time_identifier",
    "geographic_level",
    "country_code",
    "country_name",
    "version",
    "establishment_type_group",
    "breakdown_topic",
    "sex",
    "ethnicity_major",
    "ethnicity_minor",
    "fsm_status",
    "sen_status",
    "disadvantage_status",
    "first_language",
    "ks2_scaled_score_group",
    "school_admission_type",
    "school_religious_character",
    "qualification_type",
    "subject",
    "grade",
    "number_achieving",
    "percentage_achieving"
FROM "dfe-19e39901-93ff-4d76-950f-4689d6c361fe"
