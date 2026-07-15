-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "column00",
    "column01",
    "column02",
    "column03",
    "column04",
    "column05",
    "column06",
    "column07",
    "column08",
    "column09",
    "column10",
    "column11",
    "column12",
    "column13",
    "column14",
    "column15",
    "column16",
    "column17",
    "column18",
    "column19",
    "column20",
    "column21",
    "column22",
    "column23",
    "column24",
    "column25",
    "column26",
    "column27",
    "column28",
    "column29",
    "column30"
FROM "sg-data-d-74edc21bac7b0aa8c4253b227a7540c3"
