SELECT
    CAST(year AS INTEGER)              AS year,
    CAST(temp_reconstructed AS DOUBLE) AS temp_reconstructed,
    CAST(temp_observed AS DOUBLE)      AS temp_observed
FROM "kyoto-cherry-blossom-temperature-reconstruction"
WHERE temp_reconstructed IS NOT NULL OR temp_observed IS NOT NULL
ORDER BY year
