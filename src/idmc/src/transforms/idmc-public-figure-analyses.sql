SELECT
    iso3,
    CAST(year AS INTEGER) AS year,
    CAST(figure_cause AS INTEGER) AS figure_cause,
    figure_cause_name,
    CAST(figure_category AS INTEGER) AS figure_category,
    figure_category_name,
    description,
    CAST(figures AS BIGINT) AS figures,
    CAST(figures_rounded AS BIGINT) AS figures_rounded
FROM "idmc-public-figure-analyses"
WHERE iso3 IS NOT NULL AND year IS NOT NULL
