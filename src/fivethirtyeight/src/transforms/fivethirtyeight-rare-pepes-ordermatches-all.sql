-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Block" AS block,
    "ForwardAsset" AS forwardasset,
    "ForwardQuantity" AS forwardquantity,
    "BackwardAsset" AS backwardasset,
    "BackwardQuantity" AS backwardquantity
FROM "fivethirtyeight-rare-pepes-ordermatches-all"
