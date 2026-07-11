-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Utility allowance factors are program adjustment factors by HUD area; the geography fields are labels for the adjustment area rather than a full county dimension.
SELECT
    "state",
    "oil",
    "natural_gas",
    "electricity",
    "water_sewer_trash",
    "col_0",
    "electric",
    "fiscal_year"
FROM "hud-muaf"
