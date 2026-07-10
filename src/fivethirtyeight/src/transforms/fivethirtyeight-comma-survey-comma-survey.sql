-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "RespondentID" AS respondentid,
    "In your opinion, which sentence is more gramatically correct?" AS in_your_opinion_which_sentence_is_more_gramatically_correct,
    "Prior to reading about it above, had you heard of the serial (or Oxford) comma?" AS prior_to_reading_about_it_above_had_you_heard_of_the_serial_or_oxford_comma,
    "How much, if at all, do you care about the use (or lack thereof) of the serial (or Oxford) comma in grammar?" AS how_much_if_at_all_do_you_care_about_the_use_or_lack_thereof_of_the_serial_or_oxford_comma_in_grammar,
    "How would you write the following sentence?" AS how_would_you_write_the_following_sentence,
    "When faced with using the word ""data"", have you ever spent time considering if the word was a singular or plural noun?" AS when_faced_with_using_the_word_data_have_you_ever_spent_time_considering_if_the_word_was_a_singular_or_plural_noun,
    "How much, if at all, do you care about the debate over the use of the word ""data"" as a singluar or plural noun?" AS how_much_if_at_all_do_you_care_about_the_debate_over_the_use_of_the_word_data_as_a_singluar_or_plural_noun,
    "In your opinion, how important or unimportant is proper use of grammar?" AS in_your_opinion_how_important_or_unimportant_is_proper_use_of_grammar,
    "Gender" AS gender,
    "Age" AS age,
    "Household Income" AS household_income,
    "Education" AS education,
    "Location (Census Region)" AS location_census_region
FROM "fivethirtyeight-comma-survey-comma-survey"
