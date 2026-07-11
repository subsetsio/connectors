-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Series codes are SDMX-style identifiers and may not be unique in the raw catalog; use the series name as the catalog row identity and keep the code as a join/filter attribute.
SELECT
    "series_code",
    "series_name",
    "unit",
    CAST("source_id" AS BIGINT) AS source_id,
    "source_name",
    "source_note",
    "source_organization",
    "topics_json"
FROM "joint-external-debt-hub-series"
