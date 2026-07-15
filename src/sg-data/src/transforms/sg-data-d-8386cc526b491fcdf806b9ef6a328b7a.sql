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
    "OtherCombinationsofMRTorPublicBus" AS othercombinationsofmrtorpublicbus,
    "TaxiOnly" AS taxionly,
    "CarOnly" AS caronly,
    "PrivateCharteredBus_VanOnly" AS privatecharteredbus_vanonly,
    "Lorry_PickupOnly" AS lorry_pickuponly,
    "Motorcycle_ScooterOnly" AS motorcycle_scooteronly,
    "Others" AS others,
    "NoTransportRequired" AS notransportrequired
FROM "sg-data-d-8386cc526b491fcdf806b9ef6a328b7a"
