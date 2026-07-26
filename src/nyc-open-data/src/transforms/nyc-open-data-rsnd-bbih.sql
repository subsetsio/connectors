-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "mbpo_organization_dfta_fy_14",
    "brief_program_description",
    "new_applicant",
    "requested_funding",
    "recommended_funding",
    "program_name",
    "address",
    "city",
    "state",
    "postcode",
    "borough",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-rsnd-bbih"
