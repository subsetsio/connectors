-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "Year" AS year,
    "Title" AS title,
    "Romanised_Title" AS romanised_title,
    "Also_Known_As" AS also_known_as,
    "Publishers" AS publishers,
    "Year_Released" AS year_released,
    "Region" AS region,
    "Platform" AS platform,
    "Rating" AS rating,
    "Decision" AS decision,
    "Decision_Date" AS decision_date,
    "Consumer_Advice" AS consumer_advice,
    "More_Info" AS more_info
FROM "sg-data-d-fb51c5304f64d01f5839ee7208f853ea"
