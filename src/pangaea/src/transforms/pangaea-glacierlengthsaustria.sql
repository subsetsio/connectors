SELECT
    "collection"::VARCHAR AS collection,
    "source_doi"::VARCHAR AS source_doi,
    "dataset_doi"::VARCHAR AS dataset_doi,
    "file_name"::VARCHAR AS file_name,
    "source_row_number"::BIGINT AS source_row_number,
    TRY_CAST(
        regexp_extract(
            max(CASE WHEN "column_name" = 'Date/Time' THEN "value" END)
                OVER (PARTITION BY "dataset_doi", "file_name", "source_row_number"),
            '([0-9]{4})',
            1
        )
        AS BIGINT
    ) AS observation_year,
    "column_position"::BIGINT AS column_position,
    "column_name"::VARCHAR AS source_column_name,
    "value"::VARCHAR AS value_text,
    "metadata_text"::VARCHAR AS metadata_text
FROM "pangaea-glacierlengthsaustria"
WHERE "record_type" = 'cell'
