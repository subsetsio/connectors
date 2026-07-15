-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "PublicBusOnly" AS publicbusonly,
    "Rail_MRT_LRT_Only" AS rail_mrt_lrt_only,
    "Rail_MRT_LRT_andPublicBusOnly" AS rail_mrt_lrt_andpublicbusonly,
    "CombinationofRail_MRT_LRT_and_orPublicBus_withOtherModes" AS combinationofrail_mrt_lrt_and_orpublicbus_withothermodes,
    "Taxi_PrivateHireCarOnly" AS taxi_privatehirecaronly,
    "CarOnly" AS caronly,
    "PrivateCharteredBus_VanOnly" AS privatecharteredbus_vanonly,
    "Lorry_PickupOnly" AS lorry_pickuponly,
    "Motorcycle_ScooterOnly" AS motorcycle_scooteronly,
    "Others" AS others,
    "NoTransportRequired" AS notransportrequired
FROM "sg-data-d-9eaccc6cc0f257cfd74d5c1ceb0fb663"
