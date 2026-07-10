-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Anonymized (floutee/blurred) individual-level survey microdata with a survey weight (poids_p); rows are not uniquely keyed and values are perturbed for privacy. Use poids_p when producing population estimates.
SELECT
    "age_flou",
    CAST("sexe" AS BIGINT) AS sexe,
    "dep_flou",
    CAST("couple_flou" AS BIGINT) AS couple_flou,
    CAST("aidant" AS BIGINT) AS aidant,
    CAST("juri" AS BIGINT) AS juri,
    "girfin_apa",
    "dateeval_apa_flou",
    "date_apad_flou",
    "axe_coh",
    "axe_ori",
    "axe_toi",
    "axe_hab",
    "axe_ali",
    "axe_eli",
    "axe_trans",
    "axe_dep",
    "axe_ext",
    "axe_com",
    "apa_flou",
    "nothpb_flou",
    "notpb_flou",
    "dechpb_apa_flou",
    "dechum_apa_flou",
    "aidehum_not_flou",
    "aidehum_heure_flou",
    "ressourc_apa_flou",
    CAST("autreaide" AS BIGINT) AS autreaide,
    CAST("aideponc" AS BIGINT) AS aideponc,
    CAST("aideaid" AS BIGINT) AS aideaid,
    CAST("aideheb" AS BIGINT) AS aideheb,
    CAST("aideacc" AS BIGINT) AS aideacc,
    CAST("aidetrans" AS BIGINT) AS aidetrans,
    CAST("aidehum" AS BIGINT) AS aidehum,
    "poids_p"
FROM "drees-beneficiaires-apa-a-domicile-base-floutee-v1"
