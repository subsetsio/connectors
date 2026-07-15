-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Thousands" AS thousands,
    "Total" AS total,
    "EthnicGroupOfHusband_Chinese" AS ethnicgroupofhusband_chinese,
    "EthnicGroupOfHusband_Malays" AS ethnicgroupofhusband_malays,
    "EthnicGroupOfHusband_Indians" AS ethnicgroupofhusband_indians,
    "EthnicGroupOfHusband_Others" AS ethnicgroupofhusband_others
FROM "sg-data-d-76569608fc49c0a056430a9ca3f2e86f"
