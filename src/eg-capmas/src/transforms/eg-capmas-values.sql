-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The table mixes annual, quarterly, and monthly observations; use the period columns or derived frequency before comparing or aggregating across time.
-- caution: The source API repeats some identical observations, so published transforms deduplicate by indicator, category, and period.
SELECT
    main_subject_id,
    sub_subject_id,
    indicator_id,
    indicator_name_en,
    category_id,
    category_en,
    category_ar,
    year,
    quarter,
    month,
    frequency,
    period_key,
    value
FROM (
    SELECT
        main_subject_id,
        sub_subject_id,
        indicator_id,
        indicator_name_en,
        category_id,
        category_en,
        category_ar,
        year,
        quarter,
        month,
        CASE
            WHEN month IS NOT NULL THEN 'monthly'
            WHEN quarter IS NOT NULL THEN 'quarterly'
            ELSE 'annual'
        END AS frequency,
        CASE
            WHEN month IS NOT NULL THEN CAST(year AS VARCHAR) || '-M' || lpad(CAST(month AS VARCHAR), 2, '0')
            WHEN quarter IS NOT NULL THEN CAST(year AS VARCHAR) || '-Q' || CAST(quarter AS VARCHAR)
            ELSE CAST(year AS VARCHAR) || '-A'
        END AS period_key,
        value
    FROM "eg-capmas-values"
    WHERE value IS NOT NULL
      AND year IS NOT NULL
      AND indicator_id IS NOT NULL
      AND category_id IS NOT NULL
)
QUALIFY row_number() OVER (
    PARTITION BY indicator_id, category_id, period_key
    ORDER BY value
) = 1
