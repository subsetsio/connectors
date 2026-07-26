-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "tri_incident_number",
    "forcetype",
    "occurrence_date",
    "incident_pct",
    "patrol_borough",
    "yearmonthshort",
    "basisforencounter"
FROM "nyc-open-data-f4tj-796d"
