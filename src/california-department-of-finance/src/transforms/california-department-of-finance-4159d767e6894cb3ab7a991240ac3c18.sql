-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID_12" AS objectid_12,
    "STATEFP" AS statefp,
    "PUMA5CE" AS puma5ce,
    "NAME" AS name,
    "JUSTIFY" AS justify,
    "POP20" AS pop20,
    "Area" AS area,
    CAST("Year" AS BIGINT) AS year,
    "region",
    "county",
    "ObjectID" AS objectid,
    "PUMA20" AS puma20,
    "puma10_1",
    "pct10_1",
    "puma10_2",
    "pct10_2",
    "puma10_3",
    "pct10_3",
    "puma10_4",
    CAST("pct10_4" AS DOUBLE) AS pct10_4,
    "count_" AS count,
    "ObjectID_1" AS objectid_1,
    "Shape__Area" AS shape_area,
    "Shape__Length" AS shape_length
FROM "california-department-of-finance-4159d767e6894cb3ab7a991240ac3c18"
