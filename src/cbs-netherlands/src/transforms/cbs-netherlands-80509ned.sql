-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Perioden" AS perioden,
    "TotaalOverheidsuitgaven_1" AS totaaloverheidsuitgaven_1,
    "TotaalOverheidsuitgavenAanOnderwijs_2" AS totaaloverheidsuitgavenaanonderwijs_2,
    "TotaalPrePrimairOnderwijs_3" AS totaalpreprimaironderwijs_3,
    "PreprimairOnderwijsEnBasisonderwijs_4" AS preprimaironderwijsenbasisonderwijs_4,
    "SpeciaalBasisOnderwijs_5" AS speciaalbasisonderwijs_5,
    "TotaalSecundairOnderwijs_6" AS totaalsecundaironderwijs_6,
    "VoortgezetOnderwijs_7" AS voortgezetonderwijs_7,
    "MiddelbaarBeroepsonderwijsEnVolwEd_8" AS middelbaarberoepsonderwijsenvolwed_8,
    "TotaalTertiairOnderwijs_9" AS totaaltertiaironderwijs_9,
    "HogerBeroepsonderwijs_10" AS hogerberoepsonderwijs_10,
    "WetenschappelijkOnderwijs_11" AS wetenschappelijkonderwijs_11,
    "TotaalOverheidsuitgavenStudietoelagen_12" AS totaaloverheidsuitgavenstudietoelagen_12,
    "TotaalSecundairOnderwijs_13" AS totaalsecundaironderwijs_13,
    "VoortgezetOnderwijs_14" AS voortgezetonderwijs_14,
    "MiddelbaarBeroepsonderwijsEnVolwEd_15" AS middelbaarberoepsonderwijsenvolwed_15,
    "TotaalTertiairOnderwijs_16" AS totaaltertiaironderwijs_16,
    "HogerBeroepsonderwijs_17" AS hogerberoepsonderwijs_17,
    "WetenschappelijkOnderwijs_18" AS wetenschappelijkonderwijs_18,
    "TotaalOverheidsuitgavenAlsVanBbp_19" AS totaaloverheidsuitgavenalsvanbbp_19,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-80509ned"
