-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are logged eruption or in-eruption observations from a community source; multiple rows can describe related observations around the same physical eruption, so aggregate with the observation flags and primary/associated identifiers in mind.
SELECT
    "eruption_id",
    "geyser_id",
    "geyser_name",
    "eruption_time_epoch",
    "eruption_time",
    "has_seconds",
    "exact",
    "near_start",
    "in_eruption",
    "electronic",
    "approximate",
    "webcam",
    "initial",
    "major",
    "minor",
    "questionable",
    "duration_text",
    "duration_seconds",
    "duration_resolution",
    "duration_modifier",
    "entrant",
    "observer",
    "eruption_comment",
    "time_updated_epoch",
    "time_entered_epoch",
    "associated_primary_id",
    "other_comments"
FROM "geysertimes-eruptions"
