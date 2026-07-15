-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "NoTransportRequired" AS notransportrequired,
    "OneModeOfTransport_PublicBusOnly" AS onemodeoftransport_publicbusonly,
    "OneModeOfTransport_PrivateCharteredBus_VanOnly" AS onemodeoftransport_privatecharteredbus_vanonly,
    "OneModeOfTransport_MRTOnly" AS onemodeoftransport_mrtonly,
    "OneModeOfTransport_CarOnly" AS onemodeoftransport_caronly,
    "OneModeOfTransport_TaxiOnly" AS onemodeoftransport_taxionly,
    "OneModeOfTransport_Lorry_PickupOnly" AS onemodeoftransport_lorry_pickuponly,
    "OneModeOfTransport_Motor_Cycle_ScooterOnly" AS onemodeoftransport_motor_cycle_scooteronly,
    "OneModeOfTransport_Others" AS onemodeoftransport_others,
    "TwoOrMoreModesOfTransport_MRTandPublicBusOnly" AS twoormoremodesoftransport_mrtandpublicbusonly,
    "TwoOrMoreModesOfTransport_MRTandCarOnly" AS twoormoremodesoftransport_mrtandcaronly,
    "TwoOrMoreModesOfTransport_Others" AS twoormoremodesoftransport_others
FROM "sg-data-d-0d1c965cd75ba1cc89717934386310b4"
