-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "projectdwid",
    "projectid",
    "hpdpbvhapyear1amount",
    "iscreditfacility",
    "acquisitionprice",
    "asisappraisalamount",
    "highestbestappraisalamount",
    "intendeduseappraisalamount",
    "isnominal"
FROM "nyc-open-data-7r6i-tdj2"
