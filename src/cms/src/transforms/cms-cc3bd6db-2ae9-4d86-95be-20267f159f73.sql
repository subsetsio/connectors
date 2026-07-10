-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Title" AS title,
    "URL" AS url,
    "Description" AS description,
    CAST("Start Date" AS TIMESTAMP) AS start_date,
    "End Date" AS end_date,
    "Time Zone" AS time_zone,
    "Related Item 1" AS related_item_1,
    "Related Item 2" AS related_item_2,
    "Related Item 3" AS related_item_3,
    "Related Item 4" AS related_item_4,
    "Related Item 5" AS related_item_5,
    "Upcoming" AS upcoming,
    CAST("Unique ID" AS BIGINT) AS unique_id
FROM "cms-cc3bd6db-2ae9-4d86-95be-20267f159f73"
