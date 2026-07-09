-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ccode1",
    "abbrev1",
    "ccode2",
    "abbrev2",
    "year",
    "dcaGeneralV1" AS dcageneralv1,
    "dcaGeneralV2" AS dcageneralv2,
    "dcaSectorV1" AS dcasectorv1,
    "dcaSectorV2" AS dcasectorv2,
    "dcaAnyV1" AS dcaanyv1,
    "dcaAnyV2" AS dcaanyv2
FROM "correlates-of-war-dca-dyadic"
