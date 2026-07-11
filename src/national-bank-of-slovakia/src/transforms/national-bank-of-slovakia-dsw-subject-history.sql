SELECT
    CAST(deputy_subject_code AS VARCHAR) AS deputy_subject_code,
    CAST(deputy_subject_name AS VARCHAR) AS deputy_subject_name,
    CAST(subject_code        AS VARCHAR) AS subject_code,
    CAST(subject_name_act    AS VARCHAR) AS subject_name_act,
    CAST(subject_name_hist   AS VARCHAR) AS subject_name_hist,
    CAST(name_from           AS VARCHAR) AS name_from,
    CAST(name_till           AS VARCHAR) AS name_till,
    CAST(valid_from          AS VARCHAR) AS valid_from,
    CAST(valid_till          AS VARCHAR) AS valid_till,
    CAST(grp_parent_name     AS VARCHAR) AS grp_parent_name,
    CAST(grp_name            AS VARCHAR) AS grp_name,
    CAST(in_grp_from         AS VARCHAR) AS in_grp_from,
    CAST(in_grp_till         AS VARCHAR) AS in_grp_till
FROM "national-bank-of-slovakia-dsw-subject-history"
