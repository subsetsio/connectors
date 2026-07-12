-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Ranks and scores describe a single Open PageRank snapshot; do not treat the table as a time series.
SELECT
    "rank",
    "domain",
    "open_page_rank"
FROM "open-pagerank-top-10-million-domains"
