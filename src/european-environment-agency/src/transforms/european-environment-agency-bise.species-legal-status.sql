SELECT
    CAST("annex" AS VARCHAR) AS "annex",
    CAST("id_eunis" AS VARCHAR) AS "id_eunis",
    CAST("legal_instrument" AS VARCHAR) AS "legal_instrument",
    CAST("legal_text" AS VARCHAR) AS "legal_text",
    CAST("url_link" AS VARCHAR) AS "url_link"
FROM "european-environment-agency-bise.species-legal-status"
