SELECT DISTINCT
    CAST(zipcode AS VARCHAR)  AS zipcode,
    CAST(hsa_num AS INTEGER)  AS hsa_num,
    CAST(hsa_city AS VARCHAR) AS hsa_city,
    CAST(hsa_state AS VARCHAR) AS hsa_state,
    CAST(hrr_num AS INTEGER)  AS hrr_num,
    CAST(hrr_city AS VARCHAR) AS hrr_city,
    CAST(hrr_state AS VARCHAR) AS hrr_state,
    CAST(vintage AS INTEGER)  AS vintage
FROM "dartmouth-atlas-of-health-care-geography-crosswalk"
WHERE zipcode IS NOT NULL
