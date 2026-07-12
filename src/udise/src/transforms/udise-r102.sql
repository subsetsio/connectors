-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_udise_report_code" AS udise_report_code,
    "_udise_report_id" AS udise_report_id,
    CAST("_udise_year_id" AS BIGINT) AS udise_year_id,
    "ner_elementary_girl",
    "ner_elementary_all",
    "ner_secondary_girl",
    "ner_elementary_boy",
    "ner_primary_girl",
    "ner_higher_secondary_all",
    "ner_higher_secondary_boy",
    "location_name",
    "ner_upper_primary_boy",
    "ner_secondary_all",
    "ner_primary_boy",
    "ner_upper_primary_girl",
    "ner_higher_secondary_girl",
    "ner_primary_all",
    "ner_secondary_boy",
    "ner_upper_primary_all"
FROM "udise-r102"
