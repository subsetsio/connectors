-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are insect occurrence records from pan trap sampling; taxonomic detail varies by record.
SELECT
    CAST("sample_id" AS BIGINT) AS sample_id,
    "occurrence_id",
    CAST("specimen_code" AS BIGINT) AS specimen_code,
    "taxon_group",
    "taxon_source",
    "english_name",
    "source_taxon_version_key",
    "taxon_standardised",
    "taxon_aggregated",
    CAST("count" AS BIGINT) AS count,
    "sex",
    "stage",
    "comment",
    "order",
    "family",
    CAST("year" AS BIGINT) AS year
FROM "uk-poms-ukpoms-1kmpantrapdata-2017-2022-insects"
