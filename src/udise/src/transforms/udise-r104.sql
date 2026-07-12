-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_udise_report_code" AS udise_report_code,
    "_udise_report_id" AS udise_report_id,
    CAST("_udise_year_id" AS BIGINT) AS udise_year_id,
    "age_specific_ner_primary_all",
    "age_specific_ner_primary_girl",
    "age_specific_ner_elementary_girl",
    "age_specific_ner_higher_secondary_boy",
    "age_specific_ner_elementary_boy",
    "age_specific_ner_secondary_all",
    "age_specific_ner_upper_primary_boy",
    "age_specific_ner_primary_boy",
    "age_specific_ner_elementary_all",
    "age_specific_ner_secondary_boy",
    "location_name",
    "age_specific_ner_higher_secondary_girl",
    "age_specific_ner_higher_secondary_all",
    "age_specific_ner_upper_primary_girl",
    "age_specific_ner_secondary_girl",
    "age_specific_ner_upper_primary_all"
FROM "udise-r104"
