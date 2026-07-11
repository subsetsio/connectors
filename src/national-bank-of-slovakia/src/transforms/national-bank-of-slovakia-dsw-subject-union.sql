SELECT
    CAST(subject_code             AS VARCHAR) AS subject_code,
    CAST(successor_subject_code   AS VARCHAR) AS successor_subject_code,
    CAST(union_date               AS VARCHAR) AS union_date,
    CAST(subject_name_act         AS VARCHAR) AS subject_name_act,
    CAST(subject_name_hist        AS VARCHAR) AS subject_name_hist,
    CAST(succ_subject_name_act    AS VARCHAR) AS succ_subject_name_act,
    CAST(succ_subject_name_hist   AS VARCHAR) AS succ_subject_name_hist,
    CAST(deputy_subject_name      AS VARCHAR) AS deputy_subject_name,
    CAST(succ_deputy_subject_name AS VARCHAR) AS succ_deputy_subject_name,
    CAST(grp_parent_name          AS VARCHAR) AS grp_parent_name,
    CAST(grp_name                 AS VARCHAR) AS grp_name
FROM "national-bank-of-slovakia-dsw-subject-union"
