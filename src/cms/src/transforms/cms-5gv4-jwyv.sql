-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Net Change in Base Operating DRG Payment Amount" AS net_change_in_base_operating_drg_payment_amount,
    CAST("Number of Hospitals Receiving this Range" AS BIGINT) AS number_of_hospitals_receiving_this_range
FROM "cms-5gv4-jwyv"
