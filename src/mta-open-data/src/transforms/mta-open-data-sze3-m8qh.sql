-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "type_of_credit",
    "bond_series",
    "ratings",
    "bpa_sale_date",
    "series_original_final_maturity",
    "principal_amount_at_issuance",
    "outstanding_fixed_rate_par",
    "outstanding_variable_rate_par",
    "outstanding_synthetic_fixed_par",
    "total_outstanding_par",
    "tic",
    "posted_date"
FROM "mta-open-data-sze3-m8qh"
