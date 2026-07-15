-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "date_of_launch",
    "date_of_tender_closing",
    "date_of_award",
    "location",
    "type_of_devt_allowed",
    "lease",
    "type_of_devt_code",
    "site_area",
    "gross_plot_ratio",
    "gross_floor_area",
    "no_of_bids",
    "successful_tenderer_name",
    "successful_tender_price",
    "psm_per_gpr_or_gfa",
    "planning_area"
FROM "sg-data-d-e225b635fbe3ecf5b378447e4b517939"
