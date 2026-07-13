-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are flower occurrences associated with pan trap sampling rather than complete site inventories.
SELECT
    CAST("sample_id" AS BIGINT) AS sample_id,
    CAST("occurrence_id" AS BIGINT) AS occurrence_id,
    "taxon_group",
    "taxon_source",
    "english_name",
    "source_taxon_version_key",
    "order",
    "family",
    "floral_unit",
    "total_floral_units",
    CAST("year" AS BIGINT) AS year
FROM "uk-poms-ukpoms-1kmpantrapdata-2017-2022-flowers"
