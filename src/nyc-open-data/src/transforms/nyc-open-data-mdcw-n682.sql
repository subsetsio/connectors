-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency_name",
    "agency_acronym",
    "agency_website",
    "first_name",
    "last_name",
    "middle_initial",
    "name_suffix",
    "office_title",
    "division_name",
    "parent_division",
    "grand_parent_division",
    "great_grand_parent_division",
    "address",
    "city",
    "state",
    "zip_code",
    "phone_1",
    "phone_2",
    "fax_1",
    "fax_2",
    "agency_primary_phone",
    "division_primary_phone",
    "section"
FROM "nyc-open-data-mdcw-n682"
