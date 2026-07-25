-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "the_geom",
    CAST("id" AS BIGINT) AS id,
    "typeyrfacid",
    "city",
    "state",
    "city_state",
    CAST("latitude" AS DOUBLE) AS latitude,
    CAST("longitude" AS DOUBLE) AS longitude,
    CAST("buff_size" AS BIGINT) AS buff_size,
    "buff_units",
    "mode",
    CAST("year" AS BIGINT) AS year,
    "airportname",
    "airportcode",
    "servicelvl",
    "hub",
    "cntysrv",
    CAST("fst" AS DOUBLE) AS fst,
    CAST("ruralsrv" AS DOUBLE) AS ruralsrv
FROM "u-s-department-of-transportation-xnub-2sc4"
