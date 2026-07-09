-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw source contains duplicate full rows for a small number of alliance dyads, so this table is published without a declared key.
SELECT
    "version4id",
    "ccode1",
    "state_name1",
    "ccode2",
    "state_name2",
    "dyad_st_day",
    "dyad_st_month",
    "dyad_st_year",
    "dyad_end_day",
    "dyad_end_month",
    "dyad_end_year",
    "left_censor",
    "right_censor",
    "defense",
    "neutrality",
    "nonaggression",
    "entente",
    "asymmetric",
    "version"
FROM "correlates-of-war-alliances-dyadic"
