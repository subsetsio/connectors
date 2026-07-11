-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    CAST("TLIST(A1)" AS BIGINT) AS tlist_a1,
    CAST("Year" AS BIGINT) AS year,
    "MajorPort" AS majorport,
    "NI Major Port" AS ni_major_port,
    "Region" AS region,
    "World Region" AS world_region,
    "Direction" AS direction,
    "Direction of flow" AS direction_of_flow,
    "CargoDescriptionU" AS cargodescriptionu,
    "Cargo Description" AS cargo_description,
    "UNIT" AS unit,
    "VALUE" AS value
FROM "nisra-port02"
