-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "LivingwithSpouse_Total_Total" AS livingwithspouse_total_total,
    "LivingwithSpouse_Total_Males" AS livingwithspouse_total_males,
    "LivingwithSpouse_Total_Females" AS livingwithspouse_total_females,
    "LivingwithSpouse_NoChildreninHousehold_Total" AS livingwithspouse_nochildreninhousehold_total,
    "LivingwithSpouse_NoChildreninHousehold_Males" AS livingwithspouse_nochildreninhousehold_males,
    "LivingwithSpouse_NoChildreninHousehold_Females" AS livingwithspouse_nochildreninhousehold_females,
    "LivingwithSpouse_WithAtLeastOneEmployedChild_Total" AS livingwithspouse_withatleastoneemployedchild_total,
    "LivingwithSpouse_WithAtLeastOneEmployedChild_Males" AS livingwithspouse_withatleastoneemployedchild_males,
    "LivingwithSpouse_WithAtLeastOneEmployedChild_Females" AS livingwithspouse_withatleastoneemployedchild_females,
    "LivingwithSpouse_WithAllNon_EmployedChildren_Total" AS livingwithspouse_withallnon_employedchildren_total,
    "LivingwithSpouse_WithAllNon_EmployedChildren_Males" AS livingwithspouse_withallnon_employedchildren_males,
    "LivingwithSpouse_WithAllNon_EmployedChildren_Females" AS livingwithspouse_withallnon_employedchildren_females,
    "LivingWithChildrenbutWithoutSpouse_Total_Total" AS livingwithchildrenbutwithoutspouse_total_total,
    "LivingWithChildrenbutWithoutSpouse_Total_Males" AS livingwithchildrenbutwithoutspouse_total_males,
    "LivingWithChildrenbutWithoutSpouse_Total_Females" AS livingwithchildrenbutwithoutspouse_total_females,
    "LivingWithChildrenbutWithoutSpouse_WithAtLeastOneEmployedChild_" AS livingwithchildrenbutwithoutspouse_withatleastoneemployedchild,
    "LivingWithChildrenbutWithoutSpouse_WithAtLeastOneEmployedChild__1" AS livingwithchildrenbutwithoutspouse_withatleastoneemployedchild_1,
    "LivingWithChildrenbutWithoutSpouse_WithAtLeastOneEmployedChild__2" AS livingwithchildrenbutwithoutspouse_withatleastoneemployedchild_2,
    "LivingWithChildrenbutWithoutSpouse_WithAllNon_EmployedChildren_" AS livingwithchildrenbutwithoutspouse_withallnon_employedchildren,
    "LivingWithChildrenbutWithoutSpouse_WithAllNon_EmployedChildren__1" AS livingwithchildrenbutwithoutspouse_withallnon_employedchildren_1,
    "LivingWithChildrenbutWithoutSpouse_WithAllNon_EmployedChildren__2" AS livingwithchildrenbutwithoutspouse_withallnon_employedchildren_2,
    "NotLivingWithSpouseorChildren_Total_Total" AS notlivingwithspouseorchildren_total_total,
    "NotLivingWithSpouseorChildren_Total_Males" AS notlivingwithspouseorchildren_total_males,
    "NotLivingWithSpouseorChildren_Total_Females" AS notlivingwithspouseorchildren_total_females,
    "NotLivingWithSpouseorChildren_One_PersonHousehold_Total" AS notlivingwithspouseorchildren_one_personhousehold_total,
    "NotLivingWithSpouseorChildren_One_PersonHousehold_Males" AS notlivingwithspouseorchildren_one_personhousehold_males,
    "NotLivingWithSpouseorChildren_One_PersonHousehold_Females" AS notlivingwithspouseorchildren_one_personhousehold_females,
    "NotLivingWithSpouseorChildren_WithOtherElderlyPersonsOnly_Total" AS notlivingwithspouseorchildren_withotherelderlypersonsonly_total,
    "NotLivingWithSpouseorChildren_WithOtherElderlyPersonsOnly_Males" AS notlivingwithspouseorchildren_withotherelderlypersonsonly_males,
    "NotLivingWithSpouseorChildren_WithOtherElderlyPersonsOnly_Femal" AS notlivingwithspouseorchildren_withotherelderlypersonsonly_femal,
    "NotLivingWithSpouseorChildren_Others_Total" AS notlivingwithspouseorchildren_others_total,
    "NotLivingWithSpouseorChildren_Others_Males" AS notlivingwithspouseorchildren_others_males,
    "NotLivingWithSpouseorChildren_Others_Females" AS notlivingwithspouseorchildren_others_females
FROM "sg-data-d-df70e7fa7d362c880d9647440f67babf"
