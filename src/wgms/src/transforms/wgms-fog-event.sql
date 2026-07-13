-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "country",
    "glacier_name",
    CAST("glacier_id" AS BIGINT) AS glacier_id,
    CAST("id" AS BIGINT) AS id,
    strptime("date", '%Y-%m-%d')::DATE AS date,
    CAST("date_unc" AS DOUBLE) AS date_unc,
    CAST("latitude" AS DOUBLE) AS latitude,
    CAST("longitude" AS DOUBLE) AS longitude,
    "description",
    CAST("surge" AS BOOLEAN) AS surge,
    CAST("calving" AS BOOLEAN) AS calving,
    CAST("flood" AS BOOLEAN) AS flood,
    CAST("avalanche" AS BOOLEAN) AS avalanche,
    CAST("rockfall" AS BOOLEAN) AS rockfall,
    CAST("debris_flow" AS BOOLEAN) AS debris_flow,
    CAST("earthquake" AS BOOLEAN) AS earthquake,
    CAST("volcanic_eruption" AS BOOLEAN) AS volcanic_eruption,
    CAST("other" AS BOOLEAN) AS other,
    "investigators",
    "agencies",
    "references",
    "remarks"
FROM "wgms-fog-event"
