-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: PRIOGRID is a grid-cell panel; aggregating cells to countries or regions requires an explicit spatial weighting choice.
SELECT
    "pgid",
    "measurement_date",
    "cru_tmp",
    "cru_pre",
    "cru_pet",
    "cshapes_cover_share",
    "cshapes_gwcode",
    "geoepr_reg_excluded",
    "bdist1",
    "bdist2",
    "bdist3",
    "ghsl_population_grid",
    "hilda_cropland",
    "hilda_forest",
    "hilda_grassland",
    "hilda_ocean",
    "hilda_pasture",
    "hilda_sparse",
    "hilda_urban",
    "hilda_water",
    "linight_mean",
    "geopko_troops_count",
    "geopko_operations_count",
    "speibase6_mean",
    "ghs_wup_degurba_urban",
    "ucdp_ged"
FROM "prio-40"
