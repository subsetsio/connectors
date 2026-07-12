-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "location_id",
    "iso",
    "location_type",
    "location_name",
    "base_years",
    "ipcc_wetlands_suplement",
    "ndc",
    "ndc_adaptation",
    "ndc_blurb",
    "ndc_mitigation",
    "ndc_reduction_target",
    "ndc_target",
    "ndc_target_url",
    "ndc_updated",
    "pledge_summary",
    "pledge_type",
    "target_years",
    CAST("frel" AS DOUBLE) AS frel,
    "year_frel",
    "fow"
FROM "global-mangrove-watch-international-status"
