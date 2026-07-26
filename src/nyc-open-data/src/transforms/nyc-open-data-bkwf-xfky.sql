-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sample_number",
    "sample_date",
    "sample_time",
    "sample_site",
    "sample_class",
    "residual_free_chlorine_mgl",
    "turbidity_ntu",
    "fluoride_mgl",
    "coliform_quantitray_mpn_100ml",
    "ecoliquantitray_mpn100ml"
FROM "nyc-open-data-bkwf-xfky"
