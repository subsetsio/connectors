-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Transparency returns contain different activity types such as meetings, gifts, hospitality, and travel; filter resource or sheet before counting records.
SELECT
    "resource",
    "sheet",
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-2673218b-0888-4617-a94e-9df90f75117f"
