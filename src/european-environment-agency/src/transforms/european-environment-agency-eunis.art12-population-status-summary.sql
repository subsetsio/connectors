SELECT
    CAST("conclusion_status_label" AS VARCHAR) AS "conclusion_status_label",
    CAST("conclusion_status_label_prev" AS VARCHAR) AS "conclusion_status_label_prev",
    CAST("season_selected" AS VARCHAR) AS "season_selected",
    CAST("seasons_reported" AS VARCHAR) AS "seasons_reported",
    CAST("short_trend" AS VARCHAR) AS "short_trend",
    CAST("speciescode" AS VARCHAR) AS "speciescode",
    CAST("speciesname" AS VARCHAR) AS "speciesname"
FROM "european-environment-agency-eunis.art12-population-status-summary"
