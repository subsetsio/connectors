-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "BothHusbandandWifeEmployed" AS bothhusbandandwifeemployed,
    "OnlyHusbandEmployed" AS onlyhusbandemployed,
    "OnlyWifeEmployed" AS onlywifeemployed,
    "BothHusbandandWifeNotEmployed" AS bothhusbandandwifenotemployed
FROM "sg-data-d-79a62f6b68600a0b86296c686e817cce"
