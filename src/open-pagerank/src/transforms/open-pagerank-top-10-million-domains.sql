SELECT
    CAST(rank AS BIGINT)            AS rank,
    domain,
    CAST(open_page_rank AS DOUBLE)  AS open_page_rank
FROM "open-pagerank-top-10-million-domains"
WHERE rank IS NOT NULL
  AND domain IS NOT NULL
  AND length(domain) > 0
