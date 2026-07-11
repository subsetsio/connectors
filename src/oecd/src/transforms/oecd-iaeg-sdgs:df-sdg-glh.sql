-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "freq",
    "reporting_type",
    "series",
    "ref_area",
    "sex",
    "age",
    "urbanisation",
    "income_wealth_quantile",
    "education_lev",
    "occupation",
    "cust_breakdown",
    "composite_breakdown",
    "disability_status",
    "activity",
    "product",
    "obs_status",
    "unit_mult",
    "unit_measure",
    "base_per",
    "nature",
    "time_detail",
    "comment_obs",
    "time_coverage",
    "upper_bound",
    "lower_bound",
    "source_detail",
    "comment_ts",
    "geo_info_url",
    "geo_info_type",
    "cust_breakdown_lb",
    "data_last_update",
    "time_period",
    "value"
FROM "oecd-iaeg-sdgs:df-sdg-glh"
