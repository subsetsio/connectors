-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "location_name",
    "location_category",
    "administrative_district",
    "_0_superintendent" AS 0_superintendent,
    "_1_removal" AS 1_removal,
    "_1_principal" AS 1_principal,
    "_1_superintendent" AS 1_superintendent,
    "_2_removal" AS 2_removal,
    "_2_principal" AS 2_principal,
    "_2_superintendent" AS 2_superintendent,
    "_3_removal" AS 3_removal,
    "_3_principal" AS 3_principal,
    "_4_removal" AS 4_removal,
    "_4_principal" AS 4_principal,
    "_4_superintendent" AS 4_superintendent,
    "_5_principal" AS 5_principal,
    "_5_superintendent" AS 5_superintendent,
    "_610_superintendent" AS 610_superintendent,
    "_1129_superintendent" AS 1129_superintendent,
    "_30_superintendent" AS 30_superintendent,
    "_3144_superintendent" AS 3144_superintendent,
    "_45_superintendent" AS 45_superintendent,
    "_4659_superintendent" AS 4659_superintendent,
    "_60_superintendent" AS 60_superintendent,
    "_6189_superintendent" AS 6189_superintendent,
    "_90_superintendent" AS 90_superintendent,
    "_91179_superintendent" AS 91179_superintendent,
    "_180_superintendent" AS 180_superintendent,
    "awaiting_hearing_or_mdr_superintendent",
    "sy1718_total_removalssuspensions"
FROM "nyc-open-data-i6ky-n2wd"
