-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source includes exact duplicated subnational score rows for some workflow, geography, and indicator combinations, so this raw score table is intentionally keyless.
-- caution: Geographic identifiers are regional or admin-unit codes rather than country ISO3 codes; use inform-countries category fields before mixing with country-level scores.
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
FROM "inform-inform-subnational-scores"
