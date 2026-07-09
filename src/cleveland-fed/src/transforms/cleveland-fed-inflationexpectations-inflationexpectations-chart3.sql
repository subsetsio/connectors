SELECT
    CAST("label" AS BIGINT) AS horizon_years,
    vintage,
    expected_inflation
FROM (
    UNPIVOT "cleveland-fed-inflationexpectations-inflationexpectations-chart3"
    ON COLUMNS(* EXCLUDE ("label"))
    INTO NAME vintage VALUE expected_inflation
)
