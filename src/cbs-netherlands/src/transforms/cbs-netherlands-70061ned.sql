-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Perioden" AS perioden,
    "TotaalLedenVakverenigingen_1" AS totaalledenvakverenigingen_1,
    "FNV_2" AS fnv_2,
    "NVV_3" AS nvv_3,
    "NKV_4" AS nkv_4,
    "CNV_5" AS cnv_5,
    "VCP_6" AS vcp_6,
    "EVC_7" AS evc_7,
    "AVC_8" AS avc_8,
    "OverigeVakverenigingen_9" AS overigevakverenigingen_9,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-70061ned"
