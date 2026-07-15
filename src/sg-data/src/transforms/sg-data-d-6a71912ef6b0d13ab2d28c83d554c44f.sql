-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "BelowSecondary" AS belowsecondary,
    "Secondary" AS secondary,
    "Post_Secondary" AS post_secondary,
    "University" AS university
FROM "sg-data-d-6a71912ef6b0d13ab2d28c83d554c44f"
