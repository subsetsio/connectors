-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "Single" AS single,
    "Married" AS married,
    "Widowed" AS widowed,
    "Divorced_Separated" AS divorced_separated
FROM "sg-data-d-fd49f069610ddac677a207bae22f0235"
