SELECT
    "collection"::VARCHAR AS collection,
    "source_doi"::VARCHAR AS source_doi,
    COALESCE("dataset_doi", "source_doi")::VARCHAR AS dataset_doi,
    COALESCE("file_name", '__source_manifest__')::VARCHAR AS file_name,
    COALESCE("source_row_number", 0)::BIGINT AS source_row_number,
    CASE
        WHEN "record_type" = 'cell' THEN TRY_CAST(
            regexp_extract(
                max(CASE WHEN "column_name" = 'Date/Time' THEN "value" END)
                    OVER (PARTITION BY "dataset_doi", "file_name", "source_row_number"),
                '([0-9]{4})',
                1
            )
            AS BIGINT
        )
        ELSE NULL::BIGINT
    END AS observation_year,
    COALESCE("column_position", 0)::BIGINT AS column_position,
    COALESCE("column_name", 'source_doi_manifest')::VARCHAR AS source_column_name,
    COALESCE("value", "source_doi")::VARCHAR AS value_text,
    "metadata_text"::VARCHAR AS metadata_text
FROM "pangaea-glacierlengthsaustria"
