-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Unnamed Column" AS BIGINT) AS unnamed_column,
    "Route_Type" AS route_type,
    CAST("count" AS BIGINT) AS count
FROM "cdc-2nf2-f75n"
