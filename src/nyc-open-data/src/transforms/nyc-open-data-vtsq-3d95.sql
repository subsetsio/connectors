-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "abuse_physical_pre",
    "abuse_lgbtq_pre",
    "dress_pre",
    "stay_relationship_pre",
    "men_control_pre",
    "share_passwords_pre",
    "solve_problems_pre",
    "bullied_pre",
    "help_friend_pre",
    "checking_texting_pre",
    "close_friends_pre",
    "continue_ask_pre",
    "hanging_out_pre",
    "engage_act_pre",
    "abuse_physical_post",
    "abuse_lgbtq_post",
    "dress_post",
    "stay_relationship_post",
    "men_control_post",
    "share_passwords_post",
    "solve_problems_post",
    "bullied_post",
    "help_friend_post",
    "engage_act_post",
    "checking_texting_post",
    "close_friends_post",
    "continue_ask_post",
    "hanging_out_post"
FROM "nyc-open-data-vtsq-3d95"
