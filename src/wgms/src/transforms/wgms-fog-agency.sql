-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "country",
    CAST("id" AS BIGINT) AS id,
    CAST("parent_agency_id" AS BIGINT) AS parent_agency_id,
    "name",
    "abbreviation",
    "alternate_name",
    "alternate_abbreviation",
    "english_name",
    "english_abbreviation",
    "url",
    "wikipedia_url",
    "wikidata_id",
    CAST("begin_year" AS BIGINT) AS begin_year,
    CAST("end_year" AS BIGINT) AS end_year,
    CAST("former_agency_id" AS BIGINT) AS former_agency_id,
    "remarks"
FROM "wgms-fog-agency"
