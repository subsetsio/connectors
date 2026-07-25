-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Лица в возрасте 15   и более" AS 15,
    "в том числе по оценке состояния своего здоровья" AS column,
    "Лица в возрасте 0 -2" AS 0_2,
    "в том числе по оценке состояния своего здоровья_2" AS 2,
    "Лица в возрасте 3 -6" AS 3_6,
    "в том числе по оценке состояния своего здоровья_3" AS 3,
    "Лица в возрасте 7 - 14" AS 7_14,
    "в том числе по оценке состояния своего здоровья_4" AS 4
FROM "rosstat-7708234640-healthregions-2021"
