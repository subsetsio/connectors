-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "project_number",
    "project_number_sequence",
    "plan_series",
    "capital_plan",
    "agency_name",
    "category_description",
    "element_description",
    "project_description",
    "latitude",
    "longitude",
    "location_indicator",
    "location",
    "georeference"
FROM "mta-open-data-wcsa-vkhf"
