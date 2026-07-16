-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Persoonskenmerken" AS persoonskenmerken,
    "Perioden" AS perioden,
    "DaklozeMensen_1" AS daklozemensen_1,
    "DaklozeMensenRelatief_2" AS daklozemensenrelatief_2,
    "Persoonskenmerken_label" AS persoonskenmerken_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-80799ned"
