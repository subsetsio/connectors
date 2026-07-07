SELECT
    CAST("year" AS BIGINT) AS year,
    month,
    source,
    CAST(refugees AS BIGINT) AS refugees,
    CAST(asylum_seekers AS BIGINT) AS asylum_seekers
FROM "unhcr-nowcasting"
WHERE refugees IS NOT NULL OR asylum_seekers IS NOT NULL
