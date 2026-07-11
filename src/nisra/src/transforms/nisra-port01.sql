-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    CAST("TLIST(A1)" AS BIGINT) AS tlist_a1,
    CAST("Year" AS BIGINT) AS year,
    "Region" AS region,
    "World region" AS world_region,
    "Direction" AS direction,
    "Direction of flow" AS direction_of_flow,
    "CargoDescription" AS cargodescription,
    "Cargo description" AS cargo_description,
    "MajorPort" AS majorport,
    "NI major port" AS ni_major_port,
    "UNIT" AS unit,
    "VALUE" AS value
FROM "nisra-port01"
