-- Diagnostic transform for a source-catalog report that currently returns no observation data.
SELECT
    'LS-5-17' AS "report_number",
    '0400' AS "subject",
    '01' AS "sort",
    'upstream_unavailable' AS "status",
    'Source catalog/viewer exists, but the verified REST data path returns no publishable observation rows.' AS "detail"
