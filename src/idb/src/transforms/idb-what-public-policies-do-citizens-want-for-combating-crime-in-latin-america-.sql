-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Year" AS BIGINT) AS year,
    "Country" AS country,
    CAST("NUMENTRE" AS BIGINT) AS numentre,
    CAST("REG" AS BIGINT) AS reg,
    CAST("City" AS BIGINT) AS city,
    "income",
    "education",
    "d_patience1",
    "employment",
    "victim",
    "d_trust_police",
    "gender",
    CAST("age" AS BIGINT) AS age,
    "ethnicity",
    "fear_crime",
    "trust_govt",
    "trust_general",
    "crime_prob",
    "corrupt_prob",
    "pov_ineq_prob",
    CAST("pol_corrupt" AS BIGINT) AS pol_corrupt,
    "pol_finance",
    "pol_qe",
    "pol_concent",
    "source_resource"
FROM "idb-what-public-policies-do-citizens-want-for-combating-crime-in-latin-america-"
