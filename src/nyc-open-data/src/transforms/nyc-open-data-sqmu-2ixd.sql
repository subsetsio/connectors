-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "agency_number",
    "report_sort",
    "agency_name",
    "line_number",
    "line_number_description",
    "fiscal_year_1",
    "year_1_forecast",
    "year_2_estimate",
    "year_3_estimate",
    "year_4_estimate"
FROM "nyc-open-data-sqmu-2ixd"
