-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "PpCode" AS ppcode,
    "DmCode" AS dmcode,
    "VaCode" AS vacode,
    "Estimate" AS estimate,
    "LSE" AS lse,
    "LowerCIB" AS lowercib,
    "UpperCIB" AS uppercib,
    "Flag" AS flag,
    "VACode_1" AS vacode_1,
    "AgCode" AS agcode,
    "RgCode" AS rgcode
FROM "statsnz-lgbt-population-of-aotearoa-new-zealand-year-ended-june-2025"
