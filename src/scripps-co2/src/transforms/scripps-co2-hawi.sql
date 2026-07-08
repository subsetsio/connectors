SELECT station,
       CAST(sample_date AS DATE)   AS date,
       CAST(depth AS DOUBLE)       AS depth,
       CAST(salinity AS DOUBLE)    AS salinity,
       CAST(temperature AS DOUBLE) AS temperature,
       CAST(d13c_dic AS DOUBLE)    AS d13c_dic,
       CAST(dic AS DOUBLE)         AS dic,
       CAST(alk AS DOUBLE)         AS alk
FROM "scripps-co2-hawi"
WHERE COALESCE(dic, alk, d13c_dic) IS NOT NULL
