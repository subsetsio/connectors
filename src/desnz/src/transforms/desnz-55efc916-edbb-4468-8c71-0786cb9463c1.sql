-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Organogram snapshots mix posts, staff counts, grades, and salary fields; compare only like-for-like resource and sheet layouts.
SELECT
    "resource",
    "sheet",
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-55efc916-edbb-4468-8c71-0786cb9463c1"
