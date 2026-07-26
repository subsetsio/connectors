-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "tri_incident_number",
    "forcetype",
    "injurylevel",
    "member_injured",
    "rank_grouped",
    "_assignment" AS assignment,
    "member_gender",
    "race"
FROM "nyc-open-data-v5jd-6wqn"
