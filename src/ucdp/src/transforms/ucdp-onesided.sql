-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "conflict_id",
    "dyad_id",
    "actor_id",
    "coalition_components",
    "actor_name",
    "actor_name_fulltext",
    "actor_name_mothertongue",
    "year",
    "best_fatality_estimate",
    "low_fatality_estimate",
    "high_fatality_estimate",
    "is_government_actor",
    "location",
    "gwno_location",
    "gwnoa",
    "region",
    "version"
FROM "ucdp-onesided"
