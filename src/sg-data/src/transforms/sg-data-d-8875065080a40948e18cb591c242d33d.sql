-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Thousands" AS thousands,
    "Total" AS total,
    "PublicBusOnly" AS publicbusonly,
    "MRTOnly" AS mrtonly,
    "MRTandPublicBusOnly" AS mrtandpublicbusonly,
    "OtherCombinationsOfMRTOrPublicBus" AS othercombinationsofmrtorpublicbus,
    "CarOnly" AS caronly,
    "PrivateCharteredBus_VanOnly" AS privatecharteredbus_vanonly,
    "Others" AS others,
    "NoTransportRequired" AS notransportrequired
FROM "sg-data-d-8875065080a40948e18cb591c242d33d"
