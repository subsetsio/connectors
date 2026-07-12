-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The table includes multiple administrative levels; filter `Level_` before comparing or counting areas.
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
