-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are geo-located disaggregated figures and can represent subnational locations or event fragments, not independent country-year totals.
SELECT
    "id",
    "iso3",
    "country",
    "geographical_region",
    "figure_cause",
    "year",
    "figure_category",
    "figure_unit",
    "reported_figures",
    "total_figures",
    "violence_type",
    "start_date",
    "start_date_accuracy",
    "end_date",
    "end_date_accuracy",
    "publishers",
    "sources",
    "sources_type",
    "event_id",
    "event_name",
    "event_cause",
    "event_main_trigger",
    "event_start_date",
    "event_end_date",
    "is_housing_destruction",
    "event_codes",
    "locations_name",
    "locations_accuracy",
    "locations_type",
    "displacement_occurred",
    "longitude",
    "latitude",
    "geometry_type"
FROM "idmc-disaggregations"
