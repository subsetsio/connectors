-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("PERIODE", '%Y-%m')::DATE AS periode,
    "PX_BOIS_GRANVRAC_TONNE" AS px_bois_granvrac_tonne,
    "PX_BOIS_GRANSACS_TONNE" AS px_bois_gransacs_tonne,
    "PX_BOIS_GRANVRAC_100KWH" AS px_bois_granvrac_100kwh,
    "PX_BOIS_GRANSACS_100KWH" AS px_bois_gransacs_100kwh
FROM "sdes-0bf930dc-bfac-4e6f-a063-ec1774c6d029"
