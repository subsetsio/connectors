SELECT DISTINCT
    CAST(datum_primjene AS DATE)                      AS date,
    valuta                                            AS currency,
    drzava                                            AS country,
    drzava_iso                                        AS country_iso,
    sifra_valute                                      AS currency_numeric,
    CAST(REPLACE(kupovni_tecaj,  ',', '.') AS DOUBLE) AS buying_rate,
    CAST(REPLACE(srednji_tecaj,  ',', '.') AS DOUBLE) AS middle_rate,
    CAST(REPLACE(prodajni_tecaj, ',', '.') AS DOUBLE) AS selling_rate,
    CAST(broj_tecajnice AS INTEGER)                   AS bulletin_number
FROM "croatian-national-bank-exchange-rates-eur"
WHERE valuta IS NOT NULL AND datum_primjene IS NOT NULL
