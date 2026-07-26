-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "object_id",
    "organization_name",
    "approved_on_street",
    "borough_name",
    "approved_from_street",
    "approved_to_street",
    "apprdayswe",
    "status_type",
    "approved_monday_open",
    "approved_monday_close",
    "approved_tuesday_open",
    "approved_tuesday_close",
    "approved_wednesday_open",
    "approved_wednesday_close",
    "approved_thursday_open",
    "approved_thursday_close",
    "approved_friday_open",
    "approved_friday_close",
    "approved_saturday_open",
    "approved_saturday_close",
    "approved_sunday_open",
    "approved_sunday_close",
    "apprstartd",
    "apprenddat",
    "shape_stle",
    "segmentidt",
    "segmentidf",
    "lionversion",
    "the_geom"
FROM "nyc-open-data-uiay-nctu"
