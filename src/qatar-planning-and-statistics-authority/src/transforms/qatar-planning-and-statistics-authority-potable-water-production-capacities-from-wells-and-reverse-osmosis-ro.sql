-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "well_fields_and_ro",
    "hqwl_labr_wmhtt_ltndh",
    "total_no_of_wells",
    "usable_wells",
    "wells_with_pumps",
    "designed_capacity_m3_day",
    "actual_average_output_m3_day",
    "remarks",
    "mlhzt"
FROM "qatar-planning-and-statistics-authority-potable-water-production-capacities-from-wells-and-reverse-osmosis-ro"
