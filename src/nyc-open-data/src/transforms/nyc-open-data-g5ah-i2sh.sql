-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "puma_public_use_microdata_sample_areas",
    "borough",
    "home_broadband_and_mobile_broadband_adoption_percentage_of_households",
    "home_broadband_and_mobile_broadband_adoption_by_quartiles_high_mediumhigh_mediumlow_low"
FROM "nyc-open-data-g5ah-i2sh"
