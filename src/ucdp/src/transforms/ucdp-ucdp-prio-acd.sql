-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "conflict_id",
    "location",
    "side_a",
    "side_a_id",
    "side_a_2nd",
    "side_b",
    "side_b_id",
    "side_b_2nd",
    "incompatibility",
    "territory_name",
    "year",
    "intensity_level",
    "cumulative_intensity",
    "type_of_conflict",
    "start_date",
    "start_prec",
    "start_date2",
    "start_prec2",
    "ep_end",
    "ep_end_date",
    "ep_end_prec",
    "gwno_a",
    "gwno_a_2nd",
    "gwno_b",
    "gwno_b_2nd",
    "gwno_loc",
    "region",
    "version"
FROM "ucdp-ucdp-prio-acd"
