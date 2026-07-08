SELECT
    var AS variable,
    varnm AS variable_label,
    varval AS code,
    varvaldesc AS description
FROM "wittgenstein-centre-recode-dictionary"
WHERE var IS NOT NULL
