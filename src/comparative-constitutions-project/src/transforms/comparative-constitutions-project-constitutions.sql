-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows describe constitutional texts in the Constitute corpus and can include current, historic, and draft texts; filter the status and in-force fields for current-law analysis.
SELECT
    "copyright",
    "country",
    "country_id",
    "date_drafted",
    "id",
    "in_force",
    "is_draft",
    "is_historic",
    "public",
    "region",
    "show",
    "title",
    "title_long",
    "title_short",
    "translator",
    "update_needed",
    "word_length",
    "word_rank",
    CAST("year_drafted" AS BIGINT) AS year_drafted,
    CAST("year_enacted" AS BIGINT) AS year_enacted,
    CAST("year_reinstated" AS BIGINT) AS year_reinstated,
    CAST("year_revised" AS BIGINT) AS year_revised,
    "year_to",
    CAST("year_updated" AS BIGINT) AS year_updated,
    "years_amended",
    "years_in_force",
    "language"
FROM "comparative-constitutions-project-constitutions"
