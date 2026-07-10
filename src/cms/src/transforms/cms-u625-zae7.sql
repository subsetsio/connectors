-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "% Change in Base Operating DRG Payment Amount" AS change_in_base_operating_drg_payment_amount,
    CAST("Number of Hospitals Receiving this % Change" AS BIGINT) AS number_of_hospitals_receiving_this_change
FROM "cms-u625-zae7"
