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
FROM "sg-data-d-ef5695e9091a277d59c94d2bb7fb595b"
