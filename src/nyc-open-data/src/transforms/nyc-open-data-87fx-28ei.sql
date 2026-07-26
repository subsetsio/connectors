-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("created", '%m/%d/%Y')::DATE AS created,
    "bic_number",
    "account_name",
    "trade_name",
    "address",
    "city",
    "state",
    "postcode",
    "phone",
    "email",
    "market",
    "application_type",
    strptime("disposition_date", '%Y-%m-%d')::DATE AS disposition_date,
    "effective_date",
    "expiration_date",
    CAST("renewal" AS BOOLEAN) AS renewal,
    strptime("export_date", '%m/%d/%Y')::DATE AS export_date,
    CAST("latitude" AS DOUBLE) AS latitude,
    CAST("longitude" AS DOUBLE) AS longitude,
    CAST("community_board" AS BIGINT) AS community_board,
    CAST("council_district" AS BIGINT) AS council_district,
    "census_tract",
    CAST("bin" AS BIGINT) AS bin,
    CAST("bbl" AS BIGINT) AS bbl,
    "nta",
    "boro"
FROM "nyc-open-data-87fx-28ei"
