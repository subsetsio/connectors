-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_udise_report_code" AS udise_report_code,
    "_udise_report_id" AS udise_report_id,
    CAST("_udise_year_id" AS BIGINT) AS udise_year_id,
    "adjusted_ner_primary_girl",
    "adjusted_ner_primary_all",
    "adjusted_ner_upper_primary_girl",
    "adjusted_ner_higher_secondary_girl",
    "adjusted_ner_upper_primary_boy",
    "adjusted_ner_upper_primary_all",
    "adjusted_ner_higher_secondary_all",
    "adjusted_ner_elementary_girl",
    "location_name",
    "adjusted_ner_secondary_all",
    "adjusted_ner_secondary_girl",
    "adjusted_ner_primary_boy",
    "adjusted_ner_elementary_all",
    "adjusted_ner_higher_secondary_boy",
    "adjusted_ner_elementary_boy",
    "adjusted_ner_secondary_boy"
FROM "udise-r103"
