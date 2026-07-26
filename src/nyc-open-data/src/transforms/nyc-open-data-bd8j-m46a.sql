-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "schedule",
    "schedule_name",
    "section_number",
    "section_name",
    "line_number",
    "line_description",
    "fiscal_year",
    "fiscal_year_1",
    "fiscal_year_2",
    "fiscal_year_3",
    "fiscal_year_4",
    "units",
    "notes"
FROM "nyc-open-data-bd8j-m46a"
