-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Coefficient" AS coefficient,
    "Forward_Linkage" AS forward_linkage,
    "Forward_CoefficientofVariation" AS forward_coefficientofvariation,
    "Backward_Linkage" AS backward_linkage,
    "Backward_CoefficientofVariation" AS backward_coefficientofvariation
FROM "sg-data-d-4a860201ce7bea944574112ec1ee9aca"
