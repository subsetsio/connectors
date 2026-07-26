-- arxiv-papers: one row per paper, the full arXiv metadata corpus.
-- Source: weekly Kaggle snapshot (Cornell-University/arxiv), see src/nodes/arxiv.py.
--
-- created_date semantics (changed 2026-07, problem 085): now the REAL v1
-- submission date from the snapshot's versions[0].created (day granularity).
-- Before the 2026-07 re-source it was month-granular (YYYY-MM-01, derived from
-- the arXiv id); that derivation remains only as a fallback for the rare
-- record without version metadata, so a small tail of rows still lands on the
-- first of the month. Column name and type are unchanged.
--
-- Dedup prefers the freshest metadata (max update_date, then most versions) so
-- stale sibling fragments from an earlier run can never shadow current rows.
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
    license,
    num_versions,
    TRY_CAST(created_date AS DATE) AS created_date,
    TRY_CAST(update_date AS DATE) AS update_date
FROM (
    SELECT
        *,
        row_number() OVER (
            PARTITION BY arxiv_id
            ORDER BY update_date DESC NULLS LAST,
                     num_versions DESC NULLS LAST,
                     arxiv_id
        ) AS _rn
    FROM "arxiv-papers"
    WHERE arxiv_id IS NOT NULL
)
WHERE _rn = 1
