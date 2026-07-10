-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The HPI master file mixes annual, quarterly, and monthly series and multiple geography levels; filter frequency, level, hpi_type, and hpi_flavor before comparing index values.
SELECT
    "hpi_type",
    "hpi_flavor",
    "frequency",
    "level",
    "place_name",
    "place_id",
    CAST("yr" AS BIGINT) AS yr,
    CAST("period" AS BIGINT) AS period,
    "index_nsa",
    "index_sa",
    "H" AS h
FROM "fhfa-hpi"
