-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Perioden" AS perioden,
    "TotaalArbeidsongeschiktheidsuitkeringen_1" AS totaalarbeidsongeschiktheidsuitkeringen_1,
    "WAOUitkeringen_2" AS waouitkeringen_2,
    "WajongUitkeringen_3" AS wajonguitkeringen_3,
    "WAZUitkeringen_4" AS wazuitkeringen_4,
    "TotaalWIAUitkeringen_5" AS totaalwiauitkeringen_5,
    "IVAUitkeringen_6" AS ivauitkeringen_6,
    "WGAUitkeringen_7" AS wgauitkeringen_7,
    "NietSeizoengecorrigeerd_8" AS nietseizoengecorrigeerd_8,
    "Seizoengecorrigeerd_9" AS seizoengecorrigeerd_9,
    "IOWUitkeringen_10" AS iowuitkeringen_10,
    "TotaalBijstandsuitkeringen_11" AS totaalbijstandsuitkeringen_11,
    "BijstandsuitkeringenTotDeAOWLeeftijd_12" AS bijstandsuitkeringentotdeaowleeftijd_12,
    "BijstandsuitkeringenVanafAOWLeeftijd_13" AS bijstandsuitkeringenvanafaowleeftijd_13,
    "IOAWUitkeringen_14" AS ioawuitkeringen_14,
    "IOAZUitkeringen_15" AS ioazuitkeringen_15,
    "AOWUitkeringen_16" AS aowuitkeringen_16,
    "AnwUitkeringen_17" AS anwuitkeringen_17,
    "AKWGerechtigden_18" AS akwgerechtigden_18,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-37789ksz"
