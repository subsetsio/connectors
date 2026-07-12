-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "conflict_id",
    "dyad_id",
    "location_inc",
    "side_a",
    "side_a_id",
    "side_a_2nd",
    "side_b",
    "side_b_id",
    "side_b_2nd",
    "incompatibility",
    "territory_name",
    "year",
    "bd_best",
    "bd_low",
    "bd_high",
    "type_of_conflict",
    "battle_location",
    "gwno_a",
    "gwno_a_2nd",
    "gwno_b",
    "gwno_b_2nd",
    "gwno_loc",
    "gwno_battle",
    "region",
    "version"
FROM "ucdp-brd-conf"
