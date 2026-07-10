-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Percentile" AS percentile,
    "Net Change in Base Operating DRG Payment Amount" AS net_change_in_base_operating_drg_payment_amount
FROM "cms-xrgf-x36b"
