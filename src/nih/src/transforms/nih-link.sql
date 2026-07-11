-- NIH RePORTER ExPORTER LINK: the publication-to-project link table. One row
-- per (PMID, PROJECT_NUMBER) pair associating a PubMed publication with an NIH
-- full project number. Raw is stringly-typed NDJSON unioned across ~46
-- calendar-year batches; the same link recurs across release-year files, so
-- rows are deduped to the distinct pair. Year is only the file partition, not a
-- row column, so this table has no temporal axis.
SELECT DISTINCT
    TRY_CAST(PMID AS BIGINT) AS pmid,
    PROJECT_NUMBER           AS project_number
FROM "nih-link"
WHERE TRY_CAST(PMID AS BIGINT) IS NOT NULL
  AND PROJECT_NUMBER IS NOT NULL
