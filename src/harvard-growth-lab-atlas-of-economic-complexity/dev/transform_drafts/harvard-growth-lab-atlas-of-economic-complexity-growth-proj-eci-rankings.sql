SELECT country_id, country_iso3_code, year, growth_proj,
       TRY_CAST(in_rankings AS BOOLEAN) AS in_rankings,
       eci_sitc, eci_rank_sitc, eci_hs92, eci_rank_hs92,
       eci_hs12, eci_rank_hs12
FROM "harvard-growth-lab-atlas-of-economic-complexity-growth-proj-eci-rankings" WHERE year IS NOT NULL
