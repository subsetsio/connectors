-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "x",
    "y",
    "unique_squirrel_id",
    "hectare",
    "shift",
    "date",
    "hectare_squirrel_number",
    "age",
    "primary_fur_color",
    "highlight_fur_color",
    "combination_of_primary_and_highlight_color",
    "color_notes",
    "_location" AS location,
    "above_ground_sighter_measurement",
    "specific_location",
    "running",
    "chasing",
    "climbing",
    "eating",
    "foraging",
    "other_activities",
    "kuks",
    "quaas",
    "moans",
    "tail_flags",
    "tail_twitches",
    "approaches",
    "indifferent",
    "runs_from",
    "other_interactions",
    "latlong"
FROM "nyc-open-data-vfnx-vebw"
