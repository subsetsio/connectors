SELECT
    region,
    region_name,
    CAST(Time AS INTEGER) AS year,
    sex,
    edu,
    edu_label,
    CAST(agest AS INTEGER) AS age_start,
    scenario,
    CAST(pop AS DOUBLE) AS population,
    CAST(births AS DOUBLE) AS births,
    CAST(emi AS DOUBLE) AS emigrants,
    CAST(imm AS DOUBLE) AS immigrants,
    CAST(deaths AS DOUBLE) AS deaths
FROM "wittgenstein-centre-projection-results"
