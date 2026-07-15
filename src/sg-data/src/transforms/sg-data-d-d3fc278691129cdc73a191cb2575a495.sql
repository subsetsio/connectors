-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "id",
    "institution_id",
    "offering_id",
    "created_at",
    "updated_at",
    "metadata",
    "is_active",
    "lead_time_hours",
    "price_in_cents"
FROM "sg-data-d-d3fc278691129cdc73a191cb2575a495"
