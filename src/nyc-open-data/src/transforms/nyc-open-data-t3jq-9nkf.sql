-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_id",
    "operational_status",
    "organization_type",
    "_name" AS name,
    "acronym",
    "name_alphabetized",
    "url",
    "alternate_or_former_names",
    "alternate_or_former_acronyms",
    "principal_officer_title",
    "principal_officer_full_name",
    "principal_officer_first_name",
    "principal_officer_last_name",
    "principal_officer_contact_url",
    "reports_to",
    "in_org_chart",
    "listed_in_nyc_gov_agency_directory"
FROM "nyc-open-data-t3jq-9nkf"
