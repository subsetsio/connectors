-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "year",
    "sex",
    "nus",
    "ntu",
    "smu",
    "sit",
    "sutd",
    "suss",
    "nie",
    "singapore_polytechnic",
    "ngee_ann_polytechnic",
    "temasek_polytechnic",
    "nanyang_polytechnic",
    "republic_polytechnic",
    "lasalle_diploma",
    "lasalle_degree",
    "nafa_diploma",
    "nafa_degree",
    "ite"
FROM "sg-data-d-437e089ba21c5221b0d42e3b2636b7f0"
