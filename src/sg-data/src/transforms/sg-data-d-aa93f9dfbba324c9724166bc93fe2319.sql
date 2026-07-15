-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_None" AS total_none,
    "Total_1Child" AS total_1child,
    "Total_2Children" AS total_2children,
    "Total_3Children" AS total_3children,
    "Total_4Children" AS total_4children,
    "Total_5OrMoreChildren" AS total_5ormorechildren,
    "BelowSecondary_Total" AS belowsecondary_total,
    "BelowSecondary_None" AS belowsecondary_none,
    "BelowSecondary_1Child" AS belowsecondary_1child,
    "BelowSecondary_2Children" AS belowsecondary_2children,
    "BelowSecondary_3Children" AS belowsecondary_3children,
    "BelowSecondary_4Children" AS belowsecondary_4children,
    "BelowSecondary_5OrMoreChildren" AS belowsecondary_5ormorechildren,
    "Secondary_Total" AS secondary_total,
    "Secondary_None" AS secondary_none,
    "Secondary_1Child" AS secondary_1child,
    "Secondary_2Children" AS secondary_2children,
    "Secondary_3Children" AS secondary_3children,
    "Secondary_4Children" AS secondary_4children,
    "Secondary_5OrMoreChildren" AS secondary_5ormorechildren,
    "Post_Secondary_Total" AS post_secondary_total,
    "Post_Secondary_None" AS post_secondary_none,
    "Post_Secondary_1Child" AS post_secondary_1child,
    "Post_Secondary_2Children" AS post_secondary_2children,
    "Post_Secondary_3Children" AS post_secondary_3children,
    "Post_Secondary_4Children" AS post_secondary_4children,
    "Post_Secondary_5OrMoreChildren" AS post_secondary_5ormorechildren,
    "University_Total" AS university_total,
    "University_None" AS university_none,
    "University_1Child" AS university_1child,
    "University_2Children" AS university_2children,
    "University_3Children" AS university_3children,
    "University_4Children" AS university_4children,
    "University_5OrMoreChildren" AS university_5ormorechildren
FROM "sg-data-d-aa93f9dfbba324c9724166bc93fe2319"
