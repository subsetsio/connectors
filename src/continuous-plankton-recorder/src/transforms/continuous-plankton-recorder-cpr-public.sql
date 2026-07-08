SELECT
    occurrenceID                       AS occurrence_id,
    eventID                            AS event_id,
    catalogNumber                      AS catalog_number,
    basisOfRecord                      AS basis_of_record,
    TRY_CAST(individualCount AS BIGINT) AS individual_count,
    lifeStage                          AS life_stage,
    occurrenceStatus                   AS occurrence_status,
    taxonID                            AS taxon_id,
    scientificNameID                   AS scientific_name_id,
    scientificName                     AS scientific_name
FROM "continuous-plankton-recorder-cpr-public"
WHERE occurrenceID IS NOT NULL
