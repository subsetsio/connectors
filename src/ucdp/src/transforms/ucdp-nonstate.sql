-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "conflict_id",
    "dyad_id",
    "org",
    "side_a_name",
    "side_a_name_fulltext",
    "side_a_name_mothertongue",
    "side_a_id",
    "side_a_components",
    "side_a_2nd",
    "gwno_a_2nd",
    "side_b_name",
    "side_b_name_fulltext",
    "side_b_name_mothertongue",
    "side_b_id",
    "side_b_components",
    "side_b_2nd",
    "gwno_b_2nd",
    "start_date",
    "start_prec",
    "start_date2",
    "start_prec2",
    "ep_end",
    "ep_end_date",
    "ep_end_prec",
    "year",
    "best_fatality_estimate",
    "low_fatality_estimate",
    "high_fatality_estimate",
    "location",
    "gwno_location",
    "region",
    "version"
FROM "ucdp-nonstate"
