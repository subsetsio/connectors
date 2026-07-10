-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "period_of_survey",
    "coicop_5_digits",
    "messzahl_berichtsmonat_jahresdurchschnitt",
    "messzahl_vormonat",
    "messzahl_vorjahresmonat_vorjahresdurchschnitt",
    "prozent_vormonat",
    "prozent_vorjahresmonat_vorjahr",
    "einfluss_vormonat",
    "einfluss_vorjahresmonat_vorjahr",
    "gewicht_berichtsmonat"
FROM "statistics-austria-ogd-vpi10-vpi-2010-1"
