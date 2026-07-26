-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "title_code",
    "examination_title",
    "examination_number",
    "application_period_start_date",
    "application_period_end_date",
    "open_competitivepromotion_qualified_incumbent_exam_qie",
    "data_current_as_of"
FROM "nyc-open-data-4ptz-hmtc"
