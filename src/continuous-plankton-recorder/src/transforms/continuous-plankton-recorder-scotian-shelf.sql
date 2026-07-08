SELECT
    occurrenceID                       AS occurrence_id,
    eventID                            AS event_id,
    catalogNumber                      AS catalog_number,
    basisOfRecord                      AS basis_of_record,
    TRY_CAST(individualCount AS BIGINT) AS individual_count,
    occurrenceStatus                   AS occurrence_status,
    taxonID                            AS taxon_id,
    scientificNameID                   AS scientific_name_id
FROM "continuous-plankton-recorder-scotian-shelf"
WHERE occurrenceID IS NOT NULL
