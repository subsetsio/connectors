SELECT
    CAST(taxonID AS BIGINT) AS taxon_id,
    any_value(scientificName) AS scientific_name,
    any_value(taxonRank) AS taxon_rank,
    any_value(taxonomicStatus) AS taxonomic_status,
    any_value(acceptedNameUsage) AS accepted_name_usage,
    any_value(kingdom) AS kingdom,
    any_value(phylum) AS phylum,
    any_value("class") AS class,
    any_value("order") AS "order",
    any_value(family) AS family,
    any_value(genus) AS genus,
    any_value(species) AS species,
    any_value(is_marine) AS is_marine,
    any_value(is_brackish) AS is_brackish,
    any_value(is_freshwater) AS is_freshwater,
    any_value(is_terrestrial) AS is_terrestrial,
    CAST(SUM(TRY_CAST(records AS BIGINT)) AS BIGINT) AS records
FROM "obis-checklist"
WHERE taxonID IS NOT NULL
GROUP BY taxonID
