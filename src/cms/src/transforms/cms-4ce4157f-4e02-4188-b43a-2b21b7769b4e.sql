-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Model Name (ID's which detail page to populate)" AS model_name_id_s_which_detail_page_to_populate,
    "Date" AS date,
    "Announced/Updated" AS announced_updated,
    "Update" AS update,
    "Link (""Learn More"")" AS link_learn_more,
    CAST("Unique ID" AS BIGINT) AS unique_id
FROM "cms-4ce4157f-4e02-4188-b43a-2b21b7769b4e"
