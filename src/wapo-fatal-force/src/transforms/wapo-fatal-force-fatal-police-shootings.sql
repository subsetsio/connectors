-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Records describe fatal police shooting deaths tracked by The Washington Post; analyses by agency require treating the agency identifiers as a multi-value field rather than summing joined agency rows as independent deaths.
SELECT
    "id",
    "date",
    "threat_type",
    "flee_status",
    "armed_with",
    "city",
    "county",
    "state",
    "latitude",
    "longitude",
    "location_precision",
    "name",
    "age",
    "gender",
    "race",
    "race_source",
    "was_mental_illness_related",
    "body_camera",
    "agency_ids"
FROM "wapo-fatal-force-fatal-police-shootings"
