-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "COUNTYFP" AS countyfp,
    "County" AS county,
    "Grand_Total_Stucture_Losses" AS grand_total_stucture_losses,
    "Single_Family_Structure" AS single_family_structure,
    "Mobile_Home_Structure" AS mobile_home_structure,
    "Multi_Family_Structure" AS multi_family_structure,
    "F2013_Total_Structure_Loss" AS f2013_total_structure_loss,
    "F2014_Total_Structure_Loss" AS f2014_total_structure_loss,
    "F2015_Total_Stucture_Loss" AS f2015_total_stucture_loss,
    "F2016_Total_Stucture_Loss" AS f2016_total_stucture_loss,
    "F2017_Total_Stucture_Loss" AS f2017_total_stucture_loss,
    "F2018_Total_Stucture_Loss" AS f2018_total_stucture_loss,
    "F2019_Total_Stucture_Loss" AS f2019_total_stucture_loss,
    "F2020_Total_Stucture_Loss" AS f2020_total_stucture_loss,
    "F2021_Total_Stucture_Loss" AS f2021_total_stucture_loss,
    "F2022_Total_Structure_Loss" AS f2022_total_structure_loss,
    "F2023_Total_Structure_Loss" AS f2023_total_structure_loss,
    "F2013_Percent_Loss_of_Total_Cou" AS f2013_percent_loss_of_total_cou,
    "F2014_Percent_Loss_of_Total_Cou" AS f2014_percent_loss_of_total_cou,
    "F2015_Percent_Loss_of_Total_Cou" AS f2015_percent_loss_of_total_cou,
    "F2016_Percent_Loss_of_Total_Cou" AS f2016_percent_loss_of_total_cou,
    "F2017_Percent_Loss_of_Total_Cou" AS f2017_percent_loss_of_total_cou,
    "F2018_Percent_Loss_of_Total_Cou" AS f2018_percent_loss_of_total_cou,
    "F2019_Percent_Loss_of_Total_Cou" AS f2019_percent_loss_of_total_cou,
    "F2020_Percent_Loss_of_Total_Cou" AS f2020_percent_loss_of_total_cou,
    "F2021_Percent_Loss_of_Total_Cou" AS f2021_percent_loss_of_total_cou,
    "F2022_Percent_Loss_of_Total_Cou" AS f2022_percent_loss_of_total_cou,
    "F2023_Percent_Loss_of_Total_Cou" AS f2023_percent_loss_of_total_cou
FROM "california-department-of-finance-f38e6e7f9e1d47deafb032a9cd73cdd8"
