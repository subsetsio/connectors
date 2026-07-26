-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "block",
    "lot",
    "bin",
    "building",
    "agency",
    "_2010_score" AS 2010_score,
    "_2010source_eui_kbtuft2" AS 2010source_eui_kbtuft2,
    "_2010_ghg_emissions_intensity_kgco2eft2" AS 2010_ghg_emissions_intensity_kgco2eft2,
    "_2014_score" AS 2014_score,
    "_2014_source_eui_kbtuft2" AS 2014_source_eui_kbtuft2,
    "_2014_ghg_emissions_intensity_kgco2eft2" AS 2014_ghg_emissions_intensity_kgco2eft2
FROM "nyc-open-data-hpid-63r5"
