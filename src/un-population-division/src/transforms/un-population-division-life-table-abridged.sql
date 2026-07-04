-- WPP2024 abridged life tables by sex (Medium variant).
-- Published only for the Medium (standard) projection variant.
SELECT
    CAST(LocID AS BIGINT) AS location_id,
    Location AS location_name,
    CAST(Time AS BIGINT) AS year,
    Sex AS sex,
    AgeGrp AS age_group,
    CAST(AgeGrpStart AS BIGINT) AS age_start,
    CAST(mx AS DOUBLE) AS central_death_rate,
    CAST(qx AS DOUBLE) AS prob_dying,
    CAST(px AS DOUBLE) AS prob_surviving,
    CAST(lx AS DOUBLE) AS survivors,
    CAST(dx AS DOUBLE) AS deaths,
    CAST(nLx AS DOUBLE) AS person_years_lived,
    CAST(Sx AS DOUBLE) AS survival_ratio,
    CAST(Tx AS DOUBLE) AS person_years_above,
    CAST(ex AS DOUBLE) AS life_expectancy,
    CAST(ax AS DOUBLE) AS avg_years_in_interval
FROM "un-population-division-life-table-abridged"
WHERE LocID IS NOT NULL AND Variant = 'Medium'
