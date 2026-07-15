-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "tender_no",
    "tender_description",
    "agency",
    "award_date",
    "tender_detail_status",
    "supplier_name",
    "awarded_amt"
FROM "sg-data-d-acde1106003906a75c3fa052592f2fcb"
