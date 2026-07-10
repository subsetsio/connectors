-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "citation_name",
    "date_signed",
    "state",
    "effective_date",
    CAST("expiration_date" AS TIMESTAMP) AS expiration_date,
    "vaccination_mandate_group",
    "vaccination_requirement_details",
    CAST("vaccination_testing_frequency" AS BIGINT) AS vaccination_testing_frequency,
    "vaccination_person_exact_term",
    "vaccination_person_definition",
    "vaccination_religious_exemption",
    "vaccination_medical_exemption",
    "vaccination_enforcement",
    "negative_test_option",
    CAST("negative_test_timeframe" AS DOUBLE) AS negative_test_timeframe,
    CAST("requires_booster" AS BOOLEAN) AS requires_booster
FROM "cdc-kw6u-z8u2"
