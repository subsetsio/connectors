SELECT
    TRY_CAST(TRIM(AOU) AS INTEGER) AS aou,
    TRIM(Region) AS region,
    TRIM("Region Name") AS region_name,
    TRIM(Species) AS species,
    TRIM(Model) AS model,
    TRIM("Credibility Code") AS credibility_code,
    TRIM("Sample Size Code") AS sample_size_code,
    TRIM("Precision Code") AS precision_code,
    TRIM("Abundance Code") AS abundance_code,
    TRIM(Significance) AS significance,
    TRY_CAST(TRIM("N Routes") AS INTEGER) AS n_routes,
    TRY_CAST(TRIM(Trend) AS DOUBLE) AS trend,
    TRY_CAST(TRIM("2.5%CI") AS DOUBLE) AS ci_lower,
    TRY_CAST(TRIM("97.5%CI") AS DOUBLE) AS ci_upper,
    TRY_CAST(TRIM("Relative Abundance") AS DOUBLE) AS relative_abundance,
    TRIM(Years) AS years
FROM "north-american-breeding-bird-survey-analysis-core-trends"
WHERE TRIM(AOU) <> ''
