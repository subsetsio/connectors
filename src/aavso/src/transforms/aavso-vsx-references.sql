SELECT
    recno,
    OID                    AS oid,
    NULLIF(TRIM(Bibcode), '') AS bibcode
FROM "aavso-vsx-references"
WHERE recno IS NOT NULL
  AND OID IS NOT NULL
  AND NULLIF(TRIM(Bibcode), '') IS NOT NULL
