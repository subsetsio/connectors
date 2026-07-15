-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "date_of_launch",
    "date_of_tender_closing_or_auction",
    "date_of_award",
    "location",
    "type_of_development_allowed",
    "site_area",
    "gross_floor_area",
    "gross_plot_ratio",
    "name_of_successful_tenderer_or_bidder",
    "successful_tender_or_auction_price",
    "remark"
FROM "sg-data-d-7a043a1e4dee8041cff62b2cdd152b03"
