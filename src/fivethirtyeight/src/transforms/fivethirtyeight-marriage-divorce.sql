-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "C0" AS c0,
    "year",
    "date",
    "all_3544",
    "HS_3544" AS hs_3544,
    "SC_3544" AS sc_3544,
    "BAp_3544" AS bap_3544,
    "BAo_3544" AS bao_3544,
    "GD_3544" AS gd_3544,
    "poor_3544",
    "mid_3544",
    "rich_3544",
    "all_4554",
    "HS_4554" AS hs_4554,
    "SC_4554" AS sc_4554,
    "BAp_4554" AS bap_4554,
    "BAo_4554" AS bao_4554,
    "GD_4554" AS gd_4554,
    "poor_4554",
    "mid_4554",
    "rich_4554"
FROM "fivethirtyeight-marriage-divorce"
