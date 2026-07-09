-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Scraped from the dashboard's Plotly figures, so unit is the figure's y-axis title and carries meaning: a page can host two figures under the same chart title plotting the same series in different units. Always filter or group by unit before comparing or aggregating value. The x observation label is not uniformly a date: most charts are ISO timestamps, some are calendar years, some are category labels, and a few charts carry long-range projections, so do not treat the table as having a single time axis.
SELECT
    "page",
    "chart",
    "series",
    "unit",
    "x",
    "value"
FROM "bruegel-china-economic-database"
