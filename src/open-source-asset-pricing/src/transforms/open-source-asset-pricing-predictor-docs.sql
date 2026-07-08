SELECT
    "Acronym"                       AS predictor,
    "LongDescription"               AS description,
    "Cat.Signal"                    AS signal_category,
    "Cat.Economic"                  AS economic_category,
    "Cat.Form"                      AS form_category,
    "Cat.Data"                      AS data_category,
    "Authors"                       AS authors,
    TRY_CAST("Year" AS INTEGER)     AS year,
    "Journal"                       AS journal,
    TRY_CAST("Sign" AS INTEGER)     AS predicted_sign,
    TRY_CAST("Return" AS DOUBLE)    AS in_sample_return,
    TRY_CAST("T-Stat" AS DOUBLE)    AS t_stat,
    "Stock Weight"                  AS stock_weight,
    TRY_CAST("SampleStartYear" AS INTEGER) AS sample_start_year,
    TRY_CAST("SampleEndYear" AS INTEGER)   AS sample_end_year
FROM "open-source-asset-pricing-predictor-docs"
WHERE "Acronym" IS NOT NULL
