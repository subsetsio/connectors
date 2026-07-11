-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Institution" AS institution,
    "Rank" AS rank,
    "Total" AS total,
    "Science" AS science,
    "Engineering" AS engineering,
    "Health" AS health
FROM "ncses-nsf26307-tab004-005"
