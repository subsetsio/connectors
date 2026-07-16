-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "RegioS" AS regios,
    "Perioden" AS perioden,
    "UitkeringsontvangersTotaal_1" AS uitkeringsontvangerstotaal_1,
    "TotDeAOWLeeftijd_2" AS totdeaowleeftijd_2,
    "VanafDeAOWLeeftijd_3" AS vanafdeaowleeftijd_3,
    "Werkloosheid_4" AS werkloosheid_4,
    "BijstandGerelateerdTotAOWLeeftijd_5" AS bijstandgerelateerdtotaowleeftijd_5,
    "BijstandGerelateerdVanafAOWLeeftijd_6" AS bijstandgerelateerdvanafaowleeftijd_6,
    "BijstandTotDeAOWLeeftijd_7" AS bijstandtotdeaowleeftijd_7,
    "ArbeidsongeschiktheidTotaal_8" AS arbeidsongeschiktheidtotaal_8,
    "WAOUitkering_9" AS waouitkering_9,
    "WIAUitkeringWGARegeling_10" AS wiauitkeringwgaregeling_10,
    "WajongUitkering_11" AS wajonguitkering_11,
    "AlgemeneOuderdomswet_12" AS algemeneouderdomswet_12,
    "RegioS_label" AS regios_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-80794ned"
