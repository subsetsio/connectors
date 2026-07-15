-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "GoodsProducingIndustries_Total" AS goodsproducingindustries_total,
    "GoodsProducingIndustries_Manufac_Turing" AS goodsproducingindustries_manufac_turing,
    "GoodsProducingIndustries_Construction" AS goodsproducingindustries_construction,
    "GoodsProducingIndustries_OtherGoodsIndustries" AS goodsproducingindustries_othergoodsindustries,
    "ServicesProducingIndustries_Total" AS servicesproducingindustries_total,
    "ServicesProducingIndustries_WholesaleandRetailTrade" AS servicesproducingindustries_wholesaleandretailtrade,
    "ServicesProducingIndustries_HotelsandRestaurants" AS servicesproducingindustries_hotelsandrestaurants,
    "ServicesProducingIndustries_TransportandCommuni_Cations" AS servicesproducingindustries_transportandcommuni_cations,
    "ServicesProducingIndustries_FinancialServices" AS servicesproducingindustries_financialservices,
    "ServicesProducingIndustries_BusinessServices" AS servicesproducingindustries_businessservices,
    "ServicesProducingIndustries_OtherServicesIndustries" AS servicesproducingindustries_otherservicesindustries
FROM "sg-data-d-92d1727190698b19025e30f244c77f49"
