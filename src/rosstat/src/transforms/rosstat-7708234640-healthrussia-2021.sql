-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw table; treat rows as source records rather than mergeable observations.
SELECT
    "ВСЕГО" AS column,
    "в том числе по оценке состояния своего здоровья" AS column_2
FROM "rosstat-7708234640-healthrussia-2021"
