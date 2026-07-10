-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "famille_d_organismes",
    "2019",
    "2021",
    "2023"
FROM "drees-tarification-geographique-dans-les-contrats-individuels"
