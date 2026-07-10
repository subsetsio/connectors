SELECT
    TRY_CAST(activity_year AS INTEGER) AS activity_year,
    msa_md,
    NULLIF(msa_md_name, '') AS msa_md_name,
    NULLIF(state, '') AS state
FROM "ffiec-msamd"
WHERE activity_year IS NOT NULL
  AND msa_md IS NOT NULL
-- one reference row per MSA/MD code per annual snapshot
QUALIFY row_number() OVER (
    PARTITION BY activity_year, msa_md
    ORDER BY state NULLS LAST, msa_md_name NULLS LAST
) = 1
