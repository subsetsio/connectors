-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "rezoning_area",
    "commitment_title",
    "map_order",
    "rezoning_policy_domain",
    "lead_agency",
    "commitment_stage",
    "statement_from_source_documentpoa",
    "original_schedule",
    "narrative"
FROM "nyc-open-data-fd95-5ihz"
