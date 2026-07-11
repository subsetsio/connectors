-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source includes duplicated score rows for some workflow, geography, and indicator combinations, so this raw score table is intentionally keyless.
-- caution: This table contains the full INFORM indicator hierarchy, including composite nodes and component indicators; filter by node_level or indicator_id before aggregating scores.
SELECT
    "workflow_id",
    "workflow_name",
    "workflow_group_name",
    "gna_year",
    "score_family",
    "geo_id",
    "indicator_id",
    "indicator_name",
    "indicator_score",
    "node_level",
    "validity_year",
    "unit",
    "note"
FROM "inform-inform-risk-scores"
