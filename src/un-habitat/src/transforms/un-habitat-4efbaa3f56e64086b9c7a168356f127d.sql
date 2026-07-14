-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: A 2006 snapshot of local-government borrowing and tax-setting powers; the two indicator columns are free-text answers, not booleans, and are not comparable across countries without reading them.
-- caution: Level_ records which tier of government the row describes, so rows for one country are not alternatives to each other.
SELECT
    "source_item_id",
    "source_title",
    "source_type",
    "source_kind",
    "source_name",
    "source_row_number",
    "Country" AS country,
    "Level_" AS level,
    "Area_Name" AS area_name,
    "Local_Government_can_borrow_mon" AS local_government_can_borrow_mon,
    "Local_Government_can_change_loc" AS local_government_can_change_loc,
    "Region" AS region,
    "ObjectId" AS objectid
FROM "un-habitat-4efbaa3f56e64086b9c7a168356f127d"
