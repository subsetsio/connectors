SELECT
    arxiv_id,
    title,
    abstract,
    authors,
    submitter,
    primary_category,
    categories,
    doi,
    journal_ref,
    report_no,
    comments,
    num_versions,
    TRY_CAST(created_date AS DATE) AS created_date
FROM (
    SELECT
        *,
        row_number() OVER (PARTITION BY arxiv_id ORDER BY arxiv_id) AS _rn
    FROM "arxiv-papers"
    WHERE arxiv_id IS NOT NULL
)
WHERE _rn = 1
