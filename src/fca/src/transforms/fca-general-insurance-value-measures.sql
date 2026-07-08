SELECT firm_name,
       product_category,
       CAST(year AS INTEGER) AS year,
       band_claims_frequency,
       band_claims_acceptance_rate,
       band_average_claims_payout,
       band_claims_complaints_pct
FROM "fca-general-insurance-value-measures"
WHERE firm_name IS NOT NULL AND year IS NOT NULL
