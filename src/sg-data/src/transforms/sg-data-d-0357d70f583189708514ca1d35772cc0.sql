-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "year",
    "title",
    "company_name",
    "language",
    "event_type",
    "performance_start_date",
    "performance_end_date",
    "venue_block_number",
    "venue_street_name",
    "venue_floor_number",
    "venue_unit_number",
    "venue_building_name",
    "synopsis",
    "rating_decision",
    "consumer_advice"
FROM "sg-data-d-0357d70f583189708514ca1d35772cc0"
