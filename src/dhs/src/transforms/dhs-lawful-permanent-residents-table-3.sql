-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `section` separates REGION aggregate rows from the COUNTRY rows they contain; summing across both double-counts.
-- caution: `category` carries a 'Total' member alongside its components — filter it out before aggregating.
-- caution: `category` names only the leading members and lumps the rest into 'All other countries', so its members are not the full universe.
-- caution: Periods are U.S. federal fiscal years (October 1 to September 30), not calendar years.
-- caution: Counts are rounded to the nearest 10 by OHSS, so component rows need not sum exactly to the published totals.
SELECT
    "topic",
    "table_label",
    "title",
    "section",
    "parent_category",
    "category",
    "description",
    CAST("breakdown" AS BIGINT) AS breakdown,
    "value",
    "value_note"
FROM "dhs-lawful-permanent-residents-table-3"
