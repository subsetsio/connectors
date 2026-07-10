-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Detailed classes of admission are nested under their broad class; `parent_category` names the broad class. Rows whose `parent_category` is empty are the broad-class subtotals, so summing all rows double-counts.
-- caution: `breakdown` carries a 'Total' member alongside its components — filter it out before aggregating.
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
    "breakdown",
    "value",
    "value_note"
FROM "dhs-lawful-permanent-residents-table-7"
