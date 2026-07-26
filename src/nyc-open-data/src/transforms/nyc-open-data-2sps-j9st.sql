-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "mocs_people_id",
    "organization_name",
    "person_first_name",
    "person_middle_name",
    "person_last_name",
    "person_name_suffix",
    "relationship_type_code",
    "doing_business_start_date",
    "doing_business_end_date"
FROM "nyc-open-data-2sps-j9st"
