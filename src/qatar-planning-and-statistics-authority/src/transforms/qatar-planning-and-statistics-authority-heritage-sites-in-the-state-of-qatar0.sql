-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "heritage_category",
    "fy_t_ltrth",
    "site_type",
    "nw_lmwq",
    "number"
FROM "qatar-planning-and-statistics-authority-heritage-sites-in-the-state-of-qatar0"
