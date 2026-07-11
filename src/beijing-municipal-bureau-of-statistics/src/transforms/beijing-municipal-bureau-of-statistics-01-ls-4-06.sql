-- Diagnostic transform for a source-catalog report that currently returns no observation data.
SELECT
    'LS-4-06' AS "report_number",
    '0900' AS "subject",
    '01' AS "sort",
    'upstream_unavailable' AS "status",
    'Source catalog/viewer exists, but the verified REST data path returns no publishable observation rows.' AS "detail"
