-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Conflict termination rows can repeat conflict episode identifiers across annual conflict attributes; do not treat conflict_id plus episode fields as unique.
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
    "gwno_a",
    "gwno_a_2nd",
    "gwno_b",
    "gwno_b_2nd",
    "gwno_loc",
    "region",
    "type_of_conflict2",
    "c_epid",
    "c_epno",
    "c_ep_startyear",
    "c_epterm",
    "c_outcome",
    "c_ep_endyear",
    "c_ependdate",
    "c_ependprec",
    "c_ep_durcount",
    "c_ep_dur",
    "version"
FROM "ucdp-term-conflict"
