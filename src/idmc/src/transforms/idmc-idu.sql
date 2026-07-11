-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Internal Displacement Updates are near-real-time preliminary event records and should not be treated as final validated GIDD annual totals.
SELECT
    "id",
    "country",
    "iso3",
    "latitude",
    "longitude",
    "centroid",
    "role",
    "displacement_type",
    "qualifier",
    "figure",
    "displacement_date",
    "displacement_start_date",
    "displacement_end_date",
    "year",
    "event_id",
    "event_name",
    "event_codes",
    "event_code_types",
    "event_start_date",
    "event_end_date",
    "category",
    "subcategory",
    "type",
    "subtype",
    "standard_popup_text",
    "standard_info_text",
    "old_id",
    "sources",
    "source_url",
    "locations_name",
    "locations_coordinates",
    "locations_accuracy",
    "locations_type",
    "displacement_occurred",
    "created_at"
FROM "idmc-idu"
