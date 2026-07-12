-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "team_abbr",
    "team_name",
    "team_id",
    "team_nick",
    "team_conf",
    "team_division",
    "team_color",
    "team_color2",
    "team_color3",
    "team_color4",
    "team_logo_wikipedia",
    "team_logo_espn",
    "team_wordmark",
    "team_conference_logo",
    "team_league_logo",
    "team_logo_squared"
FROM "nflfastr-teams-colors-logos"
