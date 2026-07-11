-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("idhod" AS BIGINT) AS idhod,
    CAST("hodnota" AS DOUBLE) AS hodnota,
    CAST("stapro_kod" AS BIGINT) AS stapro_kod,
    CAST("typezar_cis" AS BIGINT) AS typezar_cis,
    CAST("typezar_kod" AS BIGINT) AS typezar_kod,
    CAST("pnet_cis" AS BIGINT) AS pnet_cis,
    "pnet_kod",
    CAST("pocdospvdom_cis" AS BIGINT) AS pocdospvdom_cis,
    CAST("pocdospvdom_kod" AS BIGINT) AS pocdospvdom_kod,
    CAST("pocdetivdom_cis" AS BIGINT) AS pocdetivdom_cis,
    CAST("pocdetivdom_kod" AS BIGINT) AS pocdetivdom_kod,
    CAST("velskupobce_cis" AS BIGINT) AS velskupobce_cis,
    CAST("velskupobce_kod" AS BIGINT) AS velskupobce_kod,
    CAST("kvartilcpdom_cis" AS BIGINT) AS kvartilcpdom_cis,
    CAST("kvartilcpdom_kod" AS BIGINT) AS kvartilcpdom_kod,
    CAST("rok" AS BIGINT) AS rok,
    CAST("uzemi_cis" AS BIGINT) AS uzemi_cis,
    CAST("uzemi_kod" AS BIGINT) AS uzemi_kod,
    "uzemi_txt",
    "stapro_txt",
    "typezar_txt",
    "pnet_text",
    "pocdospvdom_txt",
    "pocdetivdom_txt",
    "velskupobce_txt",
    "kvartilcpdom_txt"
FROM "czech-statistical-office-060003"
