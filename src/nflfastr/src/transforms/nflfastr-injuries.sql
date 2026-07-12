-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Injury report rows are status reports over time, not distinct injury episodes.
SELECT
    "season",
    "game_type",
    "team",
    "week",
    "gsis_id",
    "position",
    "full_name",
    "first_name",
    "last_name",
    "report_primary_injury",
    "report_secondary_injury",
    "report_status",
    "practice_primary_injury",
    "practice_secondary_injury",
    "practice_status",
    "date_modified",
    "season_type"
FROM "nflfastr-injuries"
