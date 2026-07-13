SELECT
    country,
    TRY_CAST(id AS BIGINT) AS agency_id,
    TRY_CAST(parent_agency_id AS BIGINT) AS parent_agency_id,
    name,
    abbreviation,
    alternate_name,
    alternate_abbreviation,
    english_name,
    english_abbreviation,
    url,
    wikipedia_url,
    wikidata_id,
    TRY_CAST(begin_year AS INTEGER) AS begin_year,
    TRY_CAST(end_year AS INTEGER) AS end_year,
    TRY_CAST(former_agency_id AS BIGINT) AS former_agency_id,
    remarks
FROM "wgms-fog-agency"
