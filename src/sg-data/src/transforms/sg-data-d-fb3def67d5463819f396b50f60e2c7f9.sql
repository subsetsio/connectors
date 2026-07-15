-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_GoodsProducingIndustries_Total" AS total_goodsproducingindustries_total,
    "Total_GoodsProducingIndustries_Manufacturing" AS total_goodsproducingindustries_manufacturing,
    "Total_GoodsProducingIndustries_Construction" AS total_goodsproducingindustries_construction,
    "Total_GoodsProducingIndustries_OtherGoodsIndustries" AS total_goodsproducingindustries_othergoodsindustries,
    "Total_ServicesProducingIndustries_Total" AS total_servicesproducingindustries_total,
    "Total_ServicesProducingIndustries_WholesaleandRetailTrade" AS total_servicesproducingindustries_wholesaleandretailtrade,
    "Total_ServicesProducingIndustries_HotelsandRestaurants" AS total_servicesproducingindustries_hotelsandrestaurants,
    "Total_ServicesProducingIndustries_TransportandCommunications" AS total_servicesproducingindustries_transportandcommunications,
    "Total_ServicesProducingIndustries_FinancialServices" AS total_servicesproducingindustries_financialservices,
    "Total_ServicesProducingIndustries_BusinessServices" AS total_servicesproducingindustries_businessservices,
    "Total_ServicesProducingIndustries_OtherServicesIndustries" AS total_servicesproducingindustries_otherservicesindustries,
    "Males_Total" AS males_total,
    "Males_GoodsProducingIndustries_Total" AS males_goodsproducingindustries_total,
    "Males_GoodsProducingIndustries_Manufacturing" AS males_goodsproducingindustries_manufacturing,
    "Males_GoodsProducingIndustries_Construction" AS males_goodsproducingindustries_construction,
    "Males_GoodsProducingIndustries_OtherGoodsIndustries" AS males_goodsproducingindustries_othergoodsindustries,
    "Males_ServicesProducingIndustries_Total" AS males_servicesproducingindustries_total,
    "Males_ServicesProducingIndustries_WholesaleandRetailTrade" AS males_servicesproducingindustries_wholesaleandretailtrade,
    "Males_ServicesProducingIndustries_HotelsandRestaurants" AS males_servicesproducingindustries_hotelsandrestaurants,
    "Males_ServicesProducingIndustries_TransportandCommunications" AS males_servicesproducingindustries_transportandcommunications,
    "Males_ServicesProducingIndustries_FinancialServices" AS males_servicesproducingindustries_financialservices,
    "Males_ServicesProducingIndustries_BusinessServices" AS males_servicesproducingindustries_businessservices,
    "Males_ServicesProducingIndustries_OtherServicesIndustries" AS males_servicesproducingindustries_otherservicesindustries,
    "Females_Total" AS females_total,
    "Females_GoodsProducingIndustries_Total" AS females_goodsproducingindustries_total,
    "Females_GoodsProducingIndustries_Manufacturing" AS females_goodsproducingindustries_manufacturing,
    "Females_GoodsProducingIndustries_Construction" AS females_goodsproducingindustries_construction,
    "Females_GoodsProducingIndustries_OtherGoodsIndustries" AS females_goodsproducingindustries_othergoodsindustries,
    "Females_ServicesProducingIndustries_Total" AS females_servicesproducingindustries_total,
    "Females_ServicesProducingIndustries_WholesaleandRetailTrade" AS females_servicesproducingindustries_wholesaleandretailtrade,
    "Females_ServicesProducingIndustries_HotelsandRestaurants" AS females_servicesproducingindustries_hotelsandrestaurants,
    "Females_ServicesProducingIndustries_TransportandCommunications" AS females_servicesproducingindustries_transportandcommunications,
    "Females_ServicesProducingIndustries_FinancialServices" AS females_servicesproducingindustries_financialservices,
    "Females_ServicesProducingIndustries_BusinessServices" AS females_servicesproducingindustries_businessservices,
    "Females_ServicesProducingIndustries_OtherServicesIndustries" AS females_servicesproducingindustries_otherservicesindustries
FROM "sg-data-d-fb3def67d5463819f396b50f60e2c7f9"
