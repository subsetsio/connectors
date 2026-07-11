-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "dd_id",
    "ref_area",
    "recipient_type",
    "fin_type",
    "currency",
    "interest_rate",
    "interest_rate_type",
    "measure",
    "dd_dim",
    "claim_rank",
    "recipient",
    "credit_prov",
    "lead_prov",
    "currency_multi",
    "ref_rate_benchmark",
    "orig_curr_value",
    "grace_period",
    "trans_repay",
    "freq",
    "repay_profile_time",
    "repo_coll",
    "fin_purpose",
    "guarantor_name",
    "guarantor_benef",
    "fin_doc_law",
    "waiver_immun",
    "dispute_res_mech",
    "embargo_time",
    "data_avail",
    "isin",
    "yield_maturity",
    "price_issuance",
    "def_event_cond",
    "trans_insur",
    "sustainability",
    "time_period",
    "value"
FROM "oecd-oecd.daf:dsd-debt-trans-ddown@df-ddown"
