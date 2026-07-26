-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_zone" AS zone,
    "district",
    "fiscal_month_number",
    "fiscal_year",
    "month_name",
    "diversion_ratetotal_total_recycling_total_waste",
    "capture_ratepaper_total_paper_max_paper",
    "capture_ratemgp_total_mgp_max_mgp",
    "capture_ratetotal_total_recycling_leaves_recycling_max_paper_max_mgpx100"
FROM "nyc-open-data-gaq9-z3hz"
