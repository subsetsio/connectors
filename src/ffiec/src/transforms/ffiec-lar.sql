SELECT
    TRY_CAST(activity_year AS INTEGER)                              AS activity_year,
    lei,
    state_code,
    county_code,                                                   -- FIPS, keep leading zeros
    census_tract,                                                  -- 11-digit GEOID, keep as text
    derived_msa_md,
    conforming_loan_limit,
    derived_loan_product_type,
    derived_dwelling_category,
    derived_ethnicity,
    derived_race,
    derived_sex,
    TRY_CAST(action_taken AS INTEGER)                              AS action_taken,
    TRY_CAST(purchaser_type AS INTEGER)                            AS purchaser_type,
    TRY_CAST(preapproval AS INTEGER)                               AS preapproval,
    TRY_CAST(loan_type AS INTEGER)                                 AS loan_type,
    TRY_CAST(loan_purpose AS INTEGER)                              AS loan_purpose,
    TRY_CAST(lien_status AS INTEGER)                               AS lien_status,
    TRY_CAST(reverse_mortgage AS INTEGER)                          AS reverse_mortgage,
    TRY_CAST(open_end_line_of_credit AS INTEGER)                   AS open_end_line_of_credit,
    TRY_CAST(business_or_commercial_purpose AS INTEGER)            AS business_or_commercial_purpose,
    TRY_CAST(loan_amount AS DOUBLE)                                AS loan_amount,
    TRY_CAST(COALESCE(combined_loan_to_value_ratio, loan_to_value_ratio) AS DOUBLE)
                                                                   AS combined_loan_to_value_ratio,
    TRY_CAST(interest_rate AS DOUBLE)                              AS interest_rate,
    TRY_CAST(rate_spread AS DOUBLE)                                AS rate_spread,
    TRY_CAST(hoepa_status AS INTEGER)                              AS hoepa_status,
    TRY_CAST(total_loan_costs AS DOUBLE)                           AS total_loan_costs,
    TRY_CAST(loan_term AS INTEGER)                                 AS loan_term,
    TRY_CAST(property_value AS DOUBLE)                             AS property_value,
    TRY_CAST(occupancy_type AS INTEGER)                            AS occupancy_type,
    total_units,                                                   -- includes ">149"/"5-24" buckets
    TRY_CAST(income AS DOUBLE)                                     AS income,
    debt_to_income_ratio,                                          -- bucketed text ("<20%", "36", ...)
    applicant_age,                                                 -- bucketed text ("25-34", ...)
    co_applicant_age,
    TRY_CAST(denial_reason_1 AS INTEGER)                           AS denial_reason_1,
    TRY_CAST(tract_population AS INTEGER)                          AS tract_population,
    TRY_CAST(tract_minority_population_percent AS DOUBLE)          AS tract_minority_population_percent,
    TRY_CAST(ffiec_msa_md_median_family_income AS INTEGER)         AS ffiec_msa_md_median_family_income,
    TRY_CAST(tract_to_msa_income_percentage AS DOUBLE)            AS tract_to_msa_income_percentage
FROM "ffiec-lar"
WHERE activity_year IS NOT NULL
  AND lei IS NOT NULL
