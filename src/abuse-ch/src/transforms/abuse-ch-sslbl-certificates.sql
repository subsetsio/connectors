SELECT
    TRY_CAST(listingdate AS TIMESTAMP)  AS listing_date,
    sha1,
    listingreason                        AS listing_reason
FROM "abuse-ch-sslbl-certificates"
WHERE sha1 IS NOT NULL
