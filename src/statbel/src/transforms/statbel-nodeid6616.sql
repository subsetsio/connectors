-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
SELECT
    "Type" AS type,
    CAST("Refnis" AS BIGINT) AS refnis,
    "Naam_gemeente" AS naam_gemeente,
    "Nom_commune" AS nom_commune,
    CAST("Code_arro" AS BIGINT) AS code_arro,
    CAST("Code_prov" AS BIGINT) AS code_prov,
    "Code_reg" AS code_reg,
    "Buffer_Zone" AS buffer_zone,
    CAST("TOT_POP" AS BIGINT) AS tot_pop,
    CAST("Niet_gelokaliseerd" AS BIGINT) AS niet_gelokaliseerd,
    CAST("TOT_POP_1" AS BIGINT) AS tot_pop_1,
    CAST("Male" AS BIGINT) AS male,
    CAST("Female" AS BIGINT) AS female,
    CAST("y0_14" AS BIGINT) AS y0_14,
    CAST("y15_64" AS BIGINT) AS y15_64,
    CAST("y65andmore" AS BIGINT) AS y65andmore,
    CAST("of_total_population" AS DOUBLE) AS of_total_population,
    CAST("of_male" AS DOUBLE) AS of_male,
    CAST("of_female" AS DOUBLE) AS of_female,
    CAST("of_y0_14" AS DOUBLE) AS of_y0_14,
    CAST("of_y15_64" AS DOUBLE) AS of_y15_64,
    CAST("of_y65andmore" AS DOUBLE) AS of_y65andmore
FROM "statbel-nodeid6616"
