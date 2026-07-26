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
    "_2010_rating" AS 2010_rating,
    "_2010_source_eui_kbtusqft" AS 2010_source_eui_kbtusqft,
    "_2010_ghg_emissions_intensity_kgco2eft2" AS 2010_ghg_emissions_intensity_kgco2eft2,
    "_2011_rating" AS 2011_rating,
    "_2011_source_eui_kbtusqft" AS 2011_source_eui_kbtusqft,
    "_2011_ghg_emissions_intensity_kgco2eft2" AS 2011_ghg_emissions_intensity_kgco2eft2,
    "_2012_rating" AS 2012_rating,
    "_2012_source_eui_kbtusqft" AS 2012_source_eui_kbtusqft,
    "_2012_ghg_emissions_intensity_kgco2eft2" AS 2012_ghg_emissions_intensity_kgco2eft2,
    "_2013_rating" AS 2013_rating,
    "_2013_source_eui_kbtusqft" AS 2013_source_eui_kbtusqft,
    "_2013_ghg_emissions_intensity_kgco2eft2" AS 2013_ghg_emissions_intensity_kgco2eft2,
    "epapmbenchmarkedas",
    "campus_name"
FROM "nyc-open-data-vvj6-d5qx"
