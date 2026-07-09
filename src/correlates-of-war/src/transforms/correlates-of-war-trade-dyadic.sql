-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ccode1",
    "ccode2",
    "year",
    "importer1",
    "importer2",
    "flow1",
    "flow2",
    "smoothflow1",
    "smoothflow2",
    "smoothtotrade",
    "spike1",
    "spike2",
    "dip1",
    "dip2",
    "trdspike",
    "tradedip",
    "bel_lux_alt_flow1",
    "bel_lux_alt_flow2",
    "china_alt_flow1",
    "china_alt_flow2",
    "source1",
    "source2",
    "version"
FROM "correlates-of-war-trade-dyadic"
