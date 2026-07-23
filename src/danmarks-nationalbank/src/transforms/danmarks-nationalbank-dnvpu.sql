-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "papir",
    "kupon",
    "valuta",
    "løbetid" AS l_betid,
    "udstedsektor",
    "udstland",
    "værdian" AS v_rdian,
    "data",
    "time",
    "value"
FROM "danmarks-nationalbank-dnvpu"
