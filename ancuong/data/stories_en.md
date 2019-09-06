## single_pad_en
* <pad>{"lang":"en"}
  - utter_pad_en
  - action_nao_say

## single_unk_en
* <unk>{"lang":"en"}
  - utter_unk_en
  - action_nao_say

## single_ask_location_en
* ask_location{"lang":"en"}
  - utter_ask_location_en
  - action_nao_say

## single_compliment_en
* compliment{"lang":"en"}
  - utter_compliment_en
  - action_nao_say

## single_ask_phone_en
* ask_phone{"lang":"en"}
  - utter_ask_phone_en
  - action_nao_say

## single_ask_ai_en
* ask_ai{"lang":"en"}
  - utter_ask_ai_en
  - action_nao_say

## single_greet_en
* greet{"lang":"en"}
  - utter_greet_en
  - action_nao_say

## single_ask_product_en
* ask_product{"lang":"en"}
  - utter_ask_product_en
  - action_nao_say

## single_ask_sale_off_en
* ask_sale_off{"lang":"en"}
  - utter_ask_sale_off_en
  - action_nao_say

## single_ask_real_person_en
* ask_real_person{"lang":"en"}
  - utter_ask_real_person_en
  - action_nao_say

## single_ask_ability_en
* ask_ability{"lang":"en"}
  - utter_ask_ability_en
  - action_nao_say

## single_goodbye_en
* goodbye{"lang":"en"}
  - utter_goodbye_en
  - action_nao_say

## single_ask_invention_en
* ask_invention{"lang":"en"}
  - utter_ask_invention_en
  - action_nao_say

## single_ask_show_en
* ask_show{"lang":"en"}
  - utter_ask_show_en
  - action_nao_say

## single_ask_health_en
* ask_health{"lang":"en"}
  - utter_ask_health_en
  - action_nao_say

## single_ask_working_hours_en
* ask_working_hours{"lang":"en"}
  - utter_ask_working_hours_en
  - action_nao_say

## single_ask_strength_en
* ask_strength{"lang":"en"}
  - utter_ask_strength_en
  - action_nao_say

## single_ask_scale_en
* ask_scale{"lang":"en"}
  - utter_ask_scale_en
  - action_nao_say

## single_rude_en
* rude{"lang":"en"}
  - utter_rude_en
  - action_nao_say

## single_ask_friends_en
* ask_friends{"lang":"en"}
  - utter_ask_friends_en
  - action_nao_say

## single_ask_name_en
* ask_name{"lang":"en"}
  - utter_ask_name_en
  - action_nao_say

## single_change_mode_en
* change_mode{"lang":"en"}
  - utter_change_mode_en
  - action_nao_say
  - action_mode

## single_ask_component_en
* ask_component{"lang":"en"}
  - utter_ask_component_en
  - action_nao_say

## single_ask_country_en
* ask_country{"lang":"en"}
  - utter_ask_country_en
  - action_nao_say

## single_affirm_en
* affirm{"lang":"en"}
  - utter_affirm_en
  - action_nao_say

## single_deny_en
* deny{"lang":"en"}
  - utter_deny_en
  - action_nao_say

## single_ask_do_something_en
* ask_do_something{"lang":"en"}
  - utter_ask_do_something_en
  - action_nao_say

## single_mood_great_en
* mood_great{"lang":"en"}
  - utter_mood_great_en
  - action_nao_say

## single_mood_unhappy_en
* mood_unhappy{"lang":"en"}
  - utter_mood_unhappy_en
  - action_nao_say

## single_ask_for_humor_en
* ask_for_humor{"lang":"en"}
  - utter_ask_for_humor_en
  - action_nao_say

<!-- Dance in list -->
## ask_entertaiment_dance_0_en
* inform_dance_name{"lang":"en"}
  - action_nao_dance_song_check
  - slot{"dance_null":"False", "dance_in_list":"True"}
  - utter_inform_dance_name_en
  - action_nao_say
  - action_nao_dance

## ask_entertaiment_dance_1_en
* ask_entertaiment{"lang":"en"}
  - action_nao_dance_song_check
  - slot{"dance_null":"False", "dance_in_list":"True"}
  - utter_inform_dance_name_en
  - action_nao_say
  - action_nao_dance

## ask_entertaiment_dance_2_en
* ask_entertaiment{"lang":"en"}
  - action_nao_dance_song_check
  - slot{"dance_null":"True"}
  - utter_ask_dance_name_en
  - action_nao_say
* inform_dance_name{"lang":"en"}
  - action_nao_dance_song_check
  - slot{"dance_null":"False", "dance_in_list":"True"}
  - utter_inform_dance_name_en
  - action_nao_say
  - action_nao_dance

<!-- Dance not in list -->
## ask_entertaiment_dance_not_0_en
* inform_dance_name{"lang":"en"}
  - action_nao_dance_song_check
  - slot{"dance_null":"False", "dance_in_list":"False"}
  - utter_song_dance_not_in_list_en
  - action_nao_say
* affirm{"lang":"en"}
  - utter_affirm_en
  - action_nao_say
  - action_random_dance
* deny{"lang":"en"}
  - utter_deny_en
  - action_nao_say

## ask_entertaiment_dance_not_1_en
* ask_entertaiment{"lang":"en"}
  - action_nao_dance_song_check
  - slot{"dance_null":"False", "dance_in_list":"False"}
  - utter_song_dance_not_in_list_en
  - action_nao_say
* affirm{"lang":"en"}
  - utter_affirm_en
  - action_nao_say
  - action_random_dance
* deny{"lang":"en"}
  - utter_deny_en
  - action_nao_say

## ask_entertaiment_dance_not_2_en
* ask_entertaiment{"lang":"en"}
  - action_nao_dance_song_check
  - slot{"dance_null":"True"}
  - utter_ask_dance_name_en
  - action_nao_say
* inform_dance_name{"lang":"en"}
  - action_nao_dance_song_check
  - slot{"dance_null":"False", "dance_in_list":"False"}
  - utter_song_dance_not_in_list_en
  - action_nao_say
* affirm{"lang":"en"}
  - utter_affirm_en
  - action_nao_say
  - action_random_dance
* deny{"lang":"en"}
  - utter_deny_en
  - action_nao_say

<!-- song in list -->
## ask_entertaiment_song_0_en
* inform_song_name{"lang":"en"}
  - action_nao_dance_song_check
  - slot{"song_null":"False", "song_in_list":"True"}
  - utter_inform_song_name_en
  - action_nao_say
  - action_nao_sing

## ask_entertaiment_song_1_en
* ask_entertaiment{"lang":"en"}
  - action_nao_dance_song_check
  - slot{"song_null":"False", "song_in_list":"True"}
  - utter_inform_song_name_en
  - action_nao_say
  - action_nao_sing

## ask_entertaiment_song_2_en
* ask_entertaiment{"lang":"en"}
  - action_nao_dance_song_check
  - slot{"song_null":"True"}
  - utter_ask_song_name_en
  - action_nao_say
* inform_song_name{"lang":"en"}
  - action_nao_dance_song_check
  - slot{"song_null":"False", "song_in_list":"True"}
  - utter_inform_song_name_en
  - action_nao_say
  - action_nao_sing

<!-- song not in list -->
## ask_entertaiment_song_not_0_en
* inform_song_name{"lang":"en"}
  - action_nao_dance_song_check
  - slot{"song_null":"False", "song_in_list":"False"}
  - utter_song_dance_not_in_list_en
  - action_nao_say
* affirm{"lang":"en"}
  - utter_affirm_en
  - action_nao_say
  - action_random_song
* deny{"lang":"en"}
  - utter_deny_en
  - action_nao_say

## ask_entertaiment_song_not_1_en
* ask_entertaiment{"lang":"en"}
  - action_nao_dance_song_check
  - slot{"song_null":"False", "song_in_list":"False"}
  - utter_song_dance_not_in_list_en
  - action_nao_say
* affirm{"lang":"en"}
  - utter_affirm_en
  - action_nao_say
  - action_random_song
* deny{"lang":"en"}
  - utter_deny_en
  - action_nao_say

## ask_entertaiment_song_not_2_en
* ask_entertaiment{"lang":"en"}
  - action_nao_dance_song_check
  - slot{"song_null":"True"}
  - utter_ask_song_name_en
  - action_nao_say
* inform_song_name{"lang":"en"}
  - action_nao_dance_song_check
  - slot{"song_null":"False", "song_in_list":"False"}
  - utter_song_dance_not_in_list_en
  - action_nao_say
* affirm{"lang":"en"}
  - utter_affirm_en
  - action_nao_say
  - action_random_song
* deny{"lang":"en"}
  - utter_deny_en
  - action_nao_say

## single_ask_wakeup_en
* ask_wakeup{"lang":"en"}
  - utter_affirm_en
  - action_nao_say
  - slot{"action":"wake"}
  - action_action

## single_ask_stop_en
* ask_stop{"lang":"en"}
  - utter_affirm_en
  - action_nao_say
  - slot{"action":"stop"}
  - action_action

## single_ask_rest_en
* ask_rest{"lang":"en"}
  - utter_affirm_en
  - action_nao_say
  - slot{"action":"rest"}
  - action_action

## single_ask_show_room_en
* ask_show_room{"lang":"en"}
  - utter_ask_show_room_en
  - action_nao_say

## single_ask_why_named_nao_en
* ask_why_named_nao{"lang":"en"}
  - utter_ask_why_named_nao_en
  - action_nao_say

## single_ask_manufactory_en
* ask_manufactory{"lang":"en"}
  - utter_ask_manufactory_en
  - action_nao_say

## single_ask_policy_en
* ask_policy{"lang":"en"}
  - utter_ask_policy_en
  - action_nao_say

## single_ask_showroom_floor_en
* ask_showroom_floor{"lang":"en"}
  - utter_ask_showroom_floor_en
  - action_nao_say

## single_ask_delivery_method_en
* ask_delivery_method{"lang":"en"}
  - utter_ask_delivery_method_en
  - action_nao_say

## single_ask_passwifi_en
* ask_passwifi{"lang":"en"}
  - utter_ask_passwifi_en
  - action_nao_say

## single_evaluate_en
* evaluate{"lang":"en"}
  - utter_evaluate_en
  - action_nao_say

## single_feedback_en
* feedback{"lang":"en"}
  - utter_feedback_en
  - action_nao_say

## single_ask_for_emotion_en
* ask_for_emotion{"lang":"en"}
  - utter_ask_for_emotion_en
  - action_nao_say

## single_thankyou_en
* thankyou{"lang":"en"}
  - utter_thankyou_en
  - action_nao_say

## single_inform_name_0_en
* inform_name{"first_name": null, "lang":"en"}
  - utter_greet_en
  - action_nao_say

## single_inform_name_1_en
* inform_name{"first_name": "hòa", "lang":"en"}
  - utter_inform_name_en
  - action_nao_say

## single_inform_age_en
* inform_age{"lang":"en"}
  - utter_inform_age_en
  - action_nao_say

## single_inform_birth_year_en
* inform_birth_year{"lang":"en"}
  - utter_inform_age_en
  - action_nao_say

## single_inform_gender_male_en
* inform_gender{"gender": "nam", "lang":"en"}
  - utter_inform_gender_male_en
  - action_nao_say

## single_inform_gender_female_en
* inform_gender{"gender": "nữ", "lang":"en"}
  - utter_inform_gender_female_en
  - action_nao_say

## single_ask_direction_en
* ask_direction{"lang":"en"}
  - utter_ask_direction_en
  - action_nao_say
