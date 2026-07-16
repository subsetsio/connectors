-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Perioden" AS perioden,
    "Huwelijksontbindingen_1" AS huwelijksontbindingen_1,
    "HuwelijksontbindingenPer1000Inwoners_2" AS huwelijksontbindingenper1000inwoners_2,
    "HuwelijksontbindingenPer1000Echtp_3" AS huwelijksontbindingenper1000echtp_3,
    "Echtscheidingen_4" AS echtscheidingen_4,
    "EchtscheidingenPer1000Inwoners_5" AS echtscheidingenper1000inwoners_5,
    "EchtscheidingenPer1000Echtparen_6" AS echtscheidingenper1000echtparen_6,
    "GemiddeldeHuwelijksduurBijEchtsch_7" AS gemiddeldehuwelijksduurbijechtsch_7,
    "TotaalEchtscheidingspercentage_8" AS totaalechtscheidingspercentage_8,
    "GemiddeldeLeeftijdMannen_9" AS gemiddeldeleeftijdmannen_9,
    "GemiddeldeLeeftijdVrouwen_10" AS gemiddeldeleeftijdvrouwen_10,
    "OverledenGehuwden_11" AS overledengehuwden_11,
    "OverledenGehuwdenPer1000Echtparen_12" AS overledengehuwdenper1000echtparen_12,
    "OverledenGehuwdeMannen_13" AS overledengehuwdemannen_13,
    "OverledenGehuwdeMannenPer1000Echtp_14" AS overledengehuwdemannenper1000echtp_14,
    "OverledenGehuwdeMannen_15" AS overledengehuwdemannen_15,
    "AchterblijvendeVrouwen_16" AS achterblijvendevrouwen_16,
    "OverledenGehuwdeVrouwen_17" AS overledengehuwdevrouwen_17,
    "OverledenGehuwdeVrouwenPer1000E_18" AS overledengehuwdevrouwenper1000e_18,
    "OverledenGehuwdeVrouwen_19" AS overledengehuwdevrouwen_19,
    "AchterblijvendeMannen_20" AS achterblijvendemannen_20,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-37425ned"
