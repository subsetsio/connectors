-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "quarter",
    "id",
    "name",
    "managed_by_agency",
    "format",
    "page_views",
    "downloads",
    "api_query",
    "subscriptions"
FROM "sg-data-d-a3ccf37872e0c9a0a3b343ee4b285369"
