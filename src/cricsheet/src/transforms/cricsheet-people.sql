-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "identifier",
    "name",
    "unique_name",
    "key_bcci",
    "key_bcci_2",
    "key_bigbash",
    "key_cricbuzz",
    "key_cricheroes",
    "key_crichq",
    "key_cricinfo",
    "key_cricinfo_2",
    "key_cricinfo_3",
    "key_cricingif",
    "key_cricketarchive",
    "key_cricketarchive_2",
    "key_cricketworld",
    "key_nvplay",
    "key_nvplay_2",
    "key_opta",
    "key_opta_2",
    "key_pulse",
    "key_pulse_2"
FROM "cricsheet-people"
