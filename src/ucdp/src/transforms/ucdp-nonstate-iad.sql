-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The issues/actors table is supplementary to non-state conflicts and can repeat dyad-year actor combinations across issue flags.
SELECT
    "dyad_id",
    "dyadid_new",
    "org",
    "year",
    "gwno_location",
    "side_a_name",
    "side_a_id",
    "side_a_live",
    "side_a_rel",
    "side_b_name",
    "side_b_id",
    "side_b_live",
    "side_b_rel",
    "dyadic_live",
    "issue_territory",
    "issue_authority",
    "issue_other",
    "subissue_agland_water",
    "subissue_religious",
    "subissue_formal_aut",
    "subissue_livestock",
    "subissue_informal_authority",
    "subissue_territory",
    "subissue_other",
    "primary",
    "secondary",
    "timeref"
FROM "ucdp-nonstate-iad"
