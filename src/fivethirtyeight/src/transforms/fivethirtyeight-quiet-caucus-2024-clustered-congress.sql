-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "icpsr",
    "name",
    "last_name",
    "party",
    "district",
    "terms_pct",
    "2020_margin",
    "cluster",
    "agreement_score",
    "progressive",
    "new_dems",
    "blue_dogs",
    "problem_solvers",
    "RMSP" AS rmsp,
    "governance",
    "study",
    "freedom",
    "dw_nominate_dim1",
    "dw_nominate_dim2",
    "notes"
FROM "fivethirtyeight-quiet-caucus-2024-clustered-congress"
