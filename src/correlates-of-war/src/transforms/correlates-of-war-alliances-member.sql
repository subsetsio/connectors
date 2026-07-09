-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "version4id",
    "ccode",
    "state_name",
    "all_st_day",
    "all_st_month",
    "all_st_year",
    "all_end_day",
    "all_end_month",
    "all_end_year",
    "ss_type",
    "mem_st_day",
    "mem_st_month",
    "mem_st_year",
    "mem_end_day",
    "mem_end_month",
    "mem_end_year",
    "left_censor",
    "right_censor",
    "defense",
    "neutrality",
    "nonaggression",
    "entente",
    "version"
FROM "correlates-of-war-alliances-member"
