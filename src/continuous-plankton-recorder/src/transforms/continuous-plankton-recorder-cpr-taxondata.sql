SELECT
    id                  AS source_row_id,
    taxonID             AS taxon_id,
    scientificNameID    AS scientific_name_id,
    acceptedNameUsageID AS accepted_name_usage_id,
    scientificName      AS scientific_name,
    taxonRank           AS taxon_rank,
    taxonRemarks        AS taxon_remarks
FROM "continuous-plankton-recorder-cpr-taxondata"
WHERE taxonID IS NOT NULL
