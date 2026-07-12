-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Financial year" AS financial_year,
    "Area" AS area,
    "Road speed" AS road_speed,
    "Road class" AS road_class,
    "Type of carriageway" AS type_of_carriageway,
    "Notes" AS notes
FROM "statswales-71410cc6-5acb-4a5e-bb68-7597cd1479dd"
