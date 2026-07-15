-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "PublicBusOnly" AS publicbusonly,
    "MRTOnly" AS mrtonly,
    "MRTandPublicBusOnly" AS mrtandpublicbusonly,
    "MRTandCarOnly" AS mrtandcaronly,
    "MRTandAnotherMode" AS mrtandanothermode,
    "TaxiOnly" AS taxionly,
    "CarOnly" AS caronly,
    "PrivateCharteredBus_VanOnly" AS privatecharteredbus_vanonly,
    "Lorry_PickupOnly" AS lorry_pickuponly,
    "Motorcycle_ScooterOnly" AS motorcycle_scooteronly,
    "Others" AS others,
    "NoTransportRequired" AS notransportrequired
FROM "sg-data-d-d8cf1d22b2c0cc96883c3846f6f1a087"
