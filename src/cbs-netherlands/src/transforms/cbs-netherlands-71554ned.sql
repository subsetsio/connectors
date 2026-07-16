-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Perioden" AS perioden,
    "TotaalEnergieaanbodTPES_1" AS totaalenergieaanbodtpes_1,
    "WinningTotaal_2" AS winningtotaal_2,
    "WinningVanSteenkool_3" AS winningvansteenkool_3,
    "WinningVanBruinkool_4" AS winningvanbruinkool_4,
    "Invoer_5" AS invoer_5,
    "Uitvoer_6" AS uitvoer_6,
    "Bunkering_7" AS bunkering_7,
    "Voorraadmutatie_8" AS voorraadmutatie_8,
    "SteenkoolbrikettenProductie_9" AS steenkoolbrikettenproductie_9,
    "ProductieTotaal_10" AS productietotaal_10,
    "ProductieUitCokesfabrieken_11" AS productieuitcokesfabrieken_11,
    "ProductieOverig_12" AS productieoverig_12,
    "ProductieOpenbareGasbedrijven_13" AS productieopenbaregasbedrijven_13,
    "AfzetOpenbareDistributiebedrijven_14" AS afzetopenbaredistributiebedrijven_14,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-71554ned"
