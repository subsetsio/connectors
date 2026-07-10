-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "CODE" AS code,
    "MFR" AS mfr,
    "MODEL" AS model,
    "TYPE-ACFT" AS type_acft,
    "TYPE-ENG" AS type_eng,
    CAST("AC-CAT" AS BIGINT) AS ac_cat,
    CAST("BUILD-CERT-IND" AS BIGINT) AS build_cert_ind,
    "NO-ENG" AS no_eng,
    "NO-SEATS" AS no_seats,
    "AC-WEIGHT" AS ac_weight,
    "SPEED" AS speed,
    "TC-DATA-SHEET" AS tc_data_sheet,
    "TC-DATA-HOLDER" AS tc_data_holder
FROM "faa-acftref"
