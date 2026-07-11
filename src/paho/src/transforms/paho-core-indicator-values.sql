-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The table mixes countries, territories, and regional aggregates in the spatial dimension; filter `spatial_dim_type` and `spatial_dim` before aggregating.
-- caution: Indicators use different units and statistic types; filter or group by `paho_indicator_id` and `type_statistics` before comparing numeric values.
SELECT
    "paho_indicator_id",
    "indicator_name",
    "nombre_indicador",
    "spatial_dim_type",
    "spatial_dim",
    "spatial_dim_en",
    "spatial_dim_es",
    "time_dim_type",
    CAST("time_dim" AS BIGINT) AS time_dim,
    "numeric_value",
    "value_as_string",
    "low",
    "high",
    "technical_note",
    "nota_tecnica",
    "data_source_type",
    "data_source_specific",
    "data_provider_type",
    "data_provider_specific",
    "data_secondary_source",
    "type_statistics",
    "public_private",
    "public_private_sp",
    "source_url",
    CAST("preliminary" AS BIGINT) AS preliminary,
    strptime("published_at", '%Y-%m-%d')::DATE AS published_at,
    strptime("accessed_at", '%Y-%m-%d')::DATE AS accessed_at
FROM "paho-core-indicator-values"
