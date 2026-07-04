-- NIH RePORTER ExPORTER PUBLICATION: one row per PubMed publication (PMID)
-- associated with NIH-funded research. Raw is stringly-typed NDJSON unioned
-- across ~46 calendar-year batches; PMID/PUB_YEAR are TRY_CAST, other fields
-- stay as source text. The QUALIFY keeps the most recent metadata if a PMID
-- recurs across release-year files. PUB_DATE stays VARCHAR (source form is
-- "2025 Nov 14" / "2025 May", not ISO); pub_year is the numeric period column.
SET arrow_large_buffer_size=true;
SELECT
    TRY_CAST(PMID AS BIGINT)      AS pmid,
    PMC_ID                        AS pmc_id,
    PUB_TITLE                     AS pub_title,
    TRY_CAST(PUB_YEAR AS INTEGER) AS pub_year,
    PUB_DATE                      AS pub_date,
    AUTHOR_LIST                   AS author_list,
    AFFILIATION                   AS affiliation,
    COUNTRY                       AS country,
    JOURNAL_TITLE                 AS journal_title,
    JOURNAL_TITLE_ABBR            AS journal_title_abbr,
    JOURNAL_VOLUME                AS journal_volume,
    JOURNAL_ISSUE                 AS journal_issue,
    ISSN                          AS issn,
    PAGE_NUMBER                   AS page_number,
    LANG                          AS lang
FROM "nih-publication"
WHERE TRY_CAST(PMID AS BIGINT) IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY TRY_CAST(PMID AS BIGINT)
    ORDER BY TRY_CAST(PUB_YEAR AS INTEGER) DESC NULLS LAST
) = 1
