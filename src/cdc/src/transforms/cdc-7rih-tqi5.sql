-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "url",
    "stratum",
    "collection",
    "series",
    "level",
    "lang",
    "dl_year_mo",
    "dl_vol_iss",
    "dl_date",
    "dl_page",
    "dl_art_num",
    "dateline",
    "base",
    "string",
    "link_canon",
    "mirror_path",
    "md_citation_doi",
    "title",
    "md_citation_categories",
    "dl_cat",
    "md_kwds",
    "md_desc",
    "md_citation_author"
FROM "cdc-7rih-tqi5"
