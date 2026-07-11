SELECT
    CAST(period              AS DATE)    AS period,
    CAST(subject_code        AS VARCHAR) AS subject_code,
    CAST(val_type            AS VARCHAR) AS val_type,
    CAST(currency            AS VARCHAR) AS currency,
    CAST(num_value           AS DOUBLE)  AS num_value,
    CAST(subject_name_act    AS VARCHAR) AS subject_name_act,
    CAST(subject_name_hist   AS VARCHAR) AS subject_name_hist,
    CAST(deputy_subject_code AS VARCHAR) AS deputy_subject_code,
    CAST(deputy_subject_name AS VARCHAR) AS deputy_subject_name,
    CAST(grp_name            AS VARCHAR) AS grp_name,
    CAST(grp_parent_name     AS VARCHAR) AS grp_parent_name
FROM "national-bank-of-slovakia-dsw-report-data"
