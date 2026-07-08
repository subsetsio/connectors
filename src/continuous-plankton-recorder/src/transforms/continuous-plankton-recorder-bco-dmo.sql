SELECT
    occurrenceID                       AS occurrence_id,
    eventID                            AS event_id,
    catalogNumber                      AS catalog_number,
    basisOfRecord                      AS basis_of_record,
    TRY_CAST(individualCount AS BIGINT) AS individual_count,
    taxonID                            AS taxon_id,
    scientificNameID                   AS scientific_name_id,
    scientificName                     AS scientific_name
FROM "continuous-plankton-recorder-bco-dmo"
WHERE occurrenceID IS NOT NULL
