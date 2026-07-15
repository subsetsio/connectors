-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "last",
    "first",
    "bat",
    "throw",
    "team",
    "g",
    "g_p",
    "g_sp",
    "g_rp",
    "g_c",
    "g_1b",
    "g_2b",
    "g_3b",
    "g_ss",
    "g_lf",
    "g_cf",
    "g_rf",
    "g_of",
    "g_dh",
    "g_ph",
    "g_pr",
    "first_g",
    "last_g",
    "season"
FROM "retrosheet-allplayers"
