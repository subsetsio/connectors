-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The AGE section holds the combined male+female totals; SEX AND AGE repeats the same age labels once under `parent_category` = 'Female' and once under 'Male'. `parent_category` is the only thing separating the two, and summing across both sections double-counts.
-- caution: Both `category` and `breakdown` carry a 'Total' member alongside their components — filter both out before aggregating.
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
FROM "dhs-nonimmigrants-table-30"
