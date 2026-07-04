-- fda-animalandveterinary-event: CVM animal & veterinary adverse-event reports; constant foreign_or_domestic ('Domestic') dropped.
SELECT
    "unique_aer_id_number" AS unique_aer_id_number,
    NULLIF(trim("report_id"), '') AS report_id,
    CAST(try_strptime("original_receive_date", '%Y%m%d') AS DATE) AS original_receive_date,
    CAST(try_strptime("onset_date", '%Y%m%d') AS DATE) AS onset_date,
    NULLIF(trim("type_of_information"), '') AS type_of_information,
    NULLIF(trim("primary_reporter"), '') AS primary_reporter,
    TRY_CAST(TRY_CAST("number_of_animals_affected" AS DOUBLE) AS BIGINT) AS number_of_animals_affected,
    TRY_CAST(TRY_CAST("number_of_animals_treated" AS DOUBLE) AS BIGINT) AS number_of_animals_treated
FROM "fda-animalandveterinary-event"
