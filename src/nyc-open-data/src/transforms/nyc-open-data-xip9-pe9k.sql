-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "title",
    "subtitle",
    "agency",
    "required_report_name",
    "additional_creators",
    "subject",
    "description",
    "date_published",
    "report_type",
    "languages",
    "associated_year_fiscal",
    "associated_year_calendar",
    "associated_borough",
    "associate_school_district",
    "associated_community_board_district",
    "associated_place",
    "filename",
    "last_modified"
FROM "nyc-open-data-xip9-pe9k"
