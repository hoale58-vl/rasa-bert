## single_pad_ja
* <pad>{"lang":"ja"}
  - utter_pad_ja
  - action_nao_say

## single_unk_ja
* <unk>{"lang":"ja"}
  - utter_unk_ja
  - action_nao_say

## single_ask_location_ja
* ask_location{"lang":"ja"}
  - utter_ask_location_ja
  - action_nao_say

## single_compliment_ja
* compliment{"lang":"ja"}
  - utter_compliment_ja
  - action_nao_say

## single_ask_phone_ja
* ask_phone{"lang":"ja"}
  - utter_ask_phone_ja
  - action_nao_say

## single_ask_ai_ja
* ask_ai{"lang":"ja"}
  - utter_ask_ai_ja
  - action_nao_say

## single_greet_ja
* greet{"lang":"ja"}
  - utter_greet_ja
  - action_nao_say

## single_ask_real_person_ja
* ask_real_person{"lang":"ja"}
  - utter_ask_real_person_ja
  - action_nao_say

## single_ask_ability_ja
* ask_ability{"lang":"ja"}
  - utter_ask_ability_ja
  - action_nao_say

## single_goodbye_ja
* goodbye{"lang":"ja"}
  - utter_goodbye_ja
  - action_nao_say

## single_ask_invention_ja
* ask_invention{"lang":"ja"}
  - utter_ask_invention_ja
  - action_nao_say

## single_ask_show_ja
* ask_show{"lang":"ja"}
  - utter_ask_show_ja
  - action_nao_say

## single_ask_health_ja
* ask_health{"lang":"ja"}
  - utter_ask_health_ja
  - action_nao_say

## single_rude_ja
* rude{"lang":"ja"}
  - utter_rude_ja
  - action_nao_say

## single_ask_friends_ja
* ask_friends{"lang":"ja"}
  - utter_ask_friends_ja
  - action_nao_say

## single_ask_name_ja
* ask_name{"lang":"ja"}
  - utter_ask_name_ja
  - action_nao_say

## single_change_mode_ja
* change_mode{"lang":"ja"}
  - utter_change_mode_ja
  - action_nao_say
  - action_mode

## single_ask_component_ja
* ask_component{"lang":"ja"}
  - utter_ask_component_ja
  - action_nao_say

## single_ask_country_ja
* ask_country{"lang":"ja"}
  - utter_ask_country_ja
  - action_nao_say

## single_affirm_ja
* affirm{"lang":"ja"}
  - utter_affirm_ja
  - action_nao_say

## single_deny_ja
* deny{"lang":"ja"}
  - utter_deny_ja
  - action_nao_say

## single_ask_do_something_ja
* ask_do_something{"lang":"ja"}
  - utter_ask_do_something_ja
  - action_nao_say

## single_mood_great_ja
* mood_great{"lang":"ja"}
  - utter_mood_great_ja
  - action_nao_say

## single_mood_unhappy_ja
* mood_unhappy{"lang":"ja"}
  - utter_mood_unhappy_ja
  - action_nao_say

## single_ask_for_humor_ja
* ask_for_humor{"lang":"ja"}
  - utter_ask_for_humor_ja
  - action_nao_say

<!-- Dance in list -->
## ask_entertaiment_dance_0_ja
* inform_dance_name{"lang":"ja"}
  - action_nao_dance_song_check
  - slot{"dance_null":"False", "dance_in_list":"True"}
  - utter_inform_dance_name_ja
  - action_nao_say
  - action_nao_dance

## ask_entertaiment_dance_1_ja
* ask_entertaiment{"lang":"ja"}
  - action_nao_dance_song_check
  - slot{"dance_null":"False", "dance_in_list":"True"}
  - utter_inform_dance_name_ja
  - action_nao_say
  - action_nao_dance

## ask_entertaiment_dance_2_ja
* ask_entertaiment{"lang":"ja"}
  - action_nao_dance_song_check
  - slot{"dance_null":"True"}
  - utter_ask_dance_name_ja
  - action_nao_say
* inform_dance_name{"lang":"ja"}
  - action_nao_dance_song_check
  - slot{"dance_null":"False", "dance_in_list":"True"}
  - utter_inform_dance_name_ja
  - action_nao_say
  - action_nao_dance

<!-- Dance not in list -->
## ask_entertaiment_dance_not_0_ja
* inform_dance_name{"lang":"ja"}
  - action_nao_dance_song_check
  - slot{"dance_null":"False", "dance_in_list":"False"}
  - utter_song_dance_not_in_list_ja
  - action_nao_say
* affirm{"lang":"ja"}
  - utter_affirm_ja
  - action_nao_say
  - action_random_dance
* deny{"lang":"ja"}
  - utter_deny_ja
  - action_nao_say

## ask_entertaiment_dance_not_1_ja
* ask_entertaiment{"lang":"ja"}
  - action_nao_dance_song_check
  - slot{"dance_null":"False", "dance_in_list":"False"}
  - utter_song_dance_not_in_list_ja
  - action_nao_say
* affirm{"lang":"ja"}
  - utter_affirm_ja
  - action_nao_say
  - action_random_dance
* deny{"lang":"ja"}
  - utter_deny_ja
  - action_nao_say

## ask_entertaiment_dance_not_2_ja
* ask_entertaiment{"lang":"ja"}
  - action_nao_dance_song_check
  - slot{"dance_null":"True"}
  - utter_ask_dance_name_ja
  - action_nao_say
* inform_dance_name{"lang":"ja"}
  - action_nao_dance_song_check
  - slot{"dance_null":"False", "dance_in_list":"False"}
  - utter_song_dance_not_in_list_ja
  - action_nao_say
* affirm{"lang":"ja"}
  - utter_affirm_ja
  - action_nao_say
  - action_random_dance
* deny{"lang":"ja"}
  - utter_deny_ja
  - action_nao_say

<!-- song in list -->
## ask_entertaiment_song_0_ja
* inform_song_name{"lang":"ja"}
  - action_nao_dance_song_check
  - slot{"song_null":"False", "song_in_list":"True"}
  - utter_inform_song_name_ja
  - action_nao_say
  - action_nao_sing

## ask_entertaiment_song_1_ja
* ask_entertaiment{"lang":"ja"}
  - action_nao_dance_song_check
  - slot{"song_null":"False", "song_in_list":"True"}
  - utter_inform_song_name_ja
  - action_nao_say
  - action_nao_sing

## ask_entertaiment_song_2_ja
* ask_entertaiment{"lang":"ja"}
  - action_nao_dance_song_check
  - slot{"song_null":"True"}
  - utter_ask_song_name_ja
  - action_nao_say
* inform_song_name{"lang":"ja"}
  - action_nao_dance_song_check
  - slot{"song_null":"False", "song_in_list":"True"}
  - utter_inform_song_name_ja
  - action_nao_say
  - action_nao_sing

<!-- song not in list -->
## ask_entertaiment_song_not_0_ja
* inform_song_name{"lang":"ja"}
  - action_nao_dance_song_check
  - slot{"song_null":"False", "song_in_list":"False"}
  - utter_song_dance_not_in_list_ja
  - action_nao_say
* affirm{"lang":"ja"}
  - utter_affirm_ja
  - action_nao_say
  - action_random_song
* deny{"lang":"ja"}
  - utter_deny_ja
  - action_nao_say

## ask_entertaiment_song_not_1_ja
* ask_entertaiment{"lang":"ja"}
  - action_nao_dance_song_check
  - slot{"song_null":"False", "song_in_list":"False"}
  - utter_song_dance_not_in_list_ja
  - action_nao_say
* affirm{"lang":"ja"}
  - utter_affirm_ja
  - action_nao_say
  - action_random_song
* deny{"lang":"ja"}
  - utter_deny_ja
  - action_nao_say

## ask_entertaiment_song_not_2_ja
* ask_entertaiment{"lang":"ja"}
  - action_nao_dance_song_check
  - slot{"song_null":"True"}
  - utter_ask_song_name_ja
  - action_nao_say
* inform_song_name{"lang":"ja"}
  - action_nao_dance_song_check
  - slot{"song_null":"False", "song_in_list":"False"}
  - utter_song_dance_not_in_list_ja
  - action_nao_say
* affirm{"lang":"ja"}
  - utter_affirm_ja
  - action_nao_say
  - action_random_song
* deny{"lang":"ja"}
  - utter_deny_ja
  - action_nao_say

## single_ask_wakeup_ja
* ask_wakeup{"lang":"ja"}
  - utter_affirm_ja
  - action_nao_say
  - slot{"action":"wake"}
  - action_action

## single_ask_stop_ja
* ask_stop{"lang":"ja"}
  - utter_affirm_ja
  - action_nao_say
  - slot{"action":"stop"}
  - action_action

## single_ask_rest_ja
* ask_rest{"lang":"ja"}
  - utter_affirm_ja
  - action_nao_say
  - slot{"action":"rest"}
  - action_action

## single_ask_why_named_nao_ja
* ask_why_named_nao{"lang":"ja"}
  - utter_ask_why_named_nao_ja
  - action_nao_say

## single_ask_passwifi_ja
* ask_passwifi{"lang":"ja"}
  - utter_ask_passwifi_ja
  - action_nao_say

## single_evaluate_ja
* evaluate{"lang":"ja"}
  - utter_evaluate_ja
  - action_nao_say

## single_feedback_ja
* feedback{"lang":"ja"}
  - utter_feedback_ja
  - action_nao_say

## single_ask_for_emotion_ja
* ask_for_emotion{"lang":"ja"}
  - utter_ask_for_emotion_ja
  - action_nao_say

## single_thankyou_ja
* thankyou{"lang":"ja"}
  - utter_thankyou_ja
  - action_nao_say

## single_inform_name_0_ja
* inform_name{"first_name": null, "lang":"ja"}
  - utter_greet_ja
  - action_nao_say

## single_inform_name_1_ja
* inform_name{"first_name": "hòa", "lang":"ja"}
  - utter_inform_name_ja
  - action_nao_say

## single_inform_age_ja
* inform_age{"lang":"ja"}
  - utter_inform_age_ja
  - action_nao_say

## single_inform_birth_year_ja
* inform_birth_year{"lang":"ja"}
  - utter_inform_age_ja
  - action_nao_say

## single_inform_gender_male_ja
* inform_gender{"gender": "nam", "lang":"ja"}
  - utter_inform_gender_male_ja
  - action_nao_say

## single_inform_gender_female_ja
* inform_gender{"gender": "nữ", "lang":"ja"}
  - utter_inform_gender_female_ja
  - action_nao_say

## single_ask_direction_ja
* ask_direction{"lang":"ja"}
  - utter_ask_direction_ja
  - action_nao_say
