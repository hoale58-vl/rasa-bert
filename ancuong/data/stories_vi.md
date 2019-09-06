## single_pad_vi
* <pad>{"lang":"vi"}
  - utter_pad_vi
  - action_nao_say

## single_unk_vi
* <unk>{"lang":"vi"}
  - utter_unk_vi
  - action_nao_say

## single_ask_location_vi
* ask_location{"lang":"vi"}
  - utter_ask_location_vi
  - action_nao_say

## single_compliment_vi
* compliment{"lang":"vi"}
  - utter_compliment_vi
  - action_nao_say

## single_ask_phone_vi
* ask_phone{"lang":"vi"}
  - utter_ask_phone_vi
  - action_nao_say

## single_ask_ai_vi
* ask_ai{"lang":"vi"}
  - utter_ask_ai_vi
  - action_nao_say

## single_greet_vi
* greet{"lang":"vi"}
  - utter_greet_vi
  - action_nao_say

## single_ask_product_vi
* ask_product{"lang":"vi"}
  - utter_ask_product_vi
  - action_nao_say

## single_ask_sale_off_vi
* ask_sale_off{"lang":"vi"}
  - utter_ask_sale_off_vi
  - action_nao_say

## single_ask_real_person_vi
* ask_real_person{"lang":"vi"}
  - utter_ask_real_person_vi
  - action_nao_say

## single_ask_ability_vi
* ask_ability{"lang":"vi"}
  - utter_ask_ability_vi
  - action_nao_say

## single_goodbye_vi
* goodbye{"lang":"vi"}
  - utter_goodbye_vi
  - action_nao_say

## single_ask_invention_vi
* ask_invention{"lang":"vi"}
  - utter_ask_invention_vi
  - action_nao_say

## single_ask_show_vi
* ask_show{"lang":"vi"}
  - utter_ask_show_vi
  - action_nao_say

## single_ask_health_vi
* ask_health{"lang":"vi"}
  - utter_ask_health_vi
  - action_nao_say

## single_ask_working_hours_vi
* ask_working_hours{"lang":"vi"}
  - utter_ask_working_hours_vi
  - action_nao_say

## single_ask_strength_vi
* ask_strength{"lang":"vi"}
  - utter_ask_strength_vi
  - action_nao_say

## single_ask_scale_vi
* ask_scale{"lang":"vi"}
  - utter_ask_scale_vi
  - action_nao_say

## single_rude_vi
* rude{"lang":"vi"}
  - utter_rude_vi
  - action_nao_say

## single_ask_friends_vi
* ask_friends{"lang":"vi"}
  - utter_ask_friends_vi
  - action_nao_say

## single_ask_name_vi
* ask_name{"lang":"vi"}
  - utter_ask_name_vi
  - action_nao_say

## single_change_mode_vi
* change_mode{"lang":"vi"}
  - utter_change_mode_vi
  - action_nao_say
  - action_mode

## single_ask_component_vi
* ask_component{"lang":"vi"}
  - utter_ask_component_vi
  - action_nao_say

## single_ask_country_vi
* ask_country{"lang":"vi"}
  - utter_ask_country_vi
  - action_nao_say

## single_affirm_vi
* affirm{"lang":"vi"}
  - utter_affirm_vi
  - action_nao_say

## single_deny_vi
* deny{"lang":"vi"}
  - utter_deny_vi
  - action_nao_say

## single_ask_do_something_vi
* ask_do_something{"lang":"vi"}
  - utter_ask_do_something_vi
  - action_nao_say

## single_mood_great_vi
* mood_great{"lang":"vi"}
  - utter_mood_great_vi
  - action_nao_say

## single_mood_unhappy_vi
* mood_unhappy{"lang":"vi"}
  - utter_mood_unhappy_vi
  - action_nao_say

## single_ask_for_humor_vi
* ask_for_humor{"lang":"vi"}
  - utter_ask_for_humor_vi
  - action_nao_say

<!-- Dance in list -->
## ask_entertaiment_dance_0_vi
* inform_dance_name{"lang":"vi"}
  - action_nao_dance_song_check
  - slot{"dance_null":"False", "dance_in_list":"True"}
  - utter_inform_dance_name_vi
  - action_nao_say
  - action_nao_dance

## ask_entertaiment_dance_1_vi
* ask_entertaiment{"lang":"vi"}
  - action_nao_dance_song_check
  - slot{"dance_null":"False", "dance_in_list":"True"}
  - utter_inform_dance_name_vi
  - action_nao_say
  - action_nao_dance

## ask_entertaiment_dance_2_vi
* ask_entertaiment{"lang":"vi"}
  - action_nao_dance_song_check
  - slot{"dance_null":"True"}
  - utter_ask_dance_name_vi
  - action_nao_say
* inform_dance_name{"lang":"vi"}
  - action_nao_dance_song_check
  - slot{"dance_null":"False", "dance_in_list":"True"}
  - utter_inform_dance_name_vi
  - action_nao_say
  - action_nao_dance

<!-- Dance not in list -->
## ask_entertaiment_dance_not_0_vi
* inform_dance_name{"lang":"vi"}
  - action_nao_dance_song_check
  - slot{"dance_null":"False", "dance_in_list":"False"}
  - utter_song_dance_not_in_list_vi
  - action_nao_say
* affirm{"lang":"vi"}
  - utter_affirm_vi
  - action_nao_say
  - action_random_dance
* deny{"lang":"vi"}
  - utter_deny_vi
  - action_nao_say

## ask_entertaiment_dance_not_1_vi
* ask_entertaiment{"lang":"vi"}
  - action_nao_dance_song_check
  - slot{"dance_null":"False", "dance_in_list":"False"}
  - utter_song_dance_not_in_list_vi
  - action_nao_say
* affirm{"lang":"vi"}
  - utter_affirm_vi
  - action_nao_say
  - action_random_dance
* deny{"lang":"vi"}
  - utter_deny_vi
  - action_nao_say

## ask_entertaiment_dance_not_2_vi
* ask_entertaiment{"lang":"vi"}
  - action_nao_dance_song_check
  - slot{"dance_null":"True"}
  - utter_ask_dance_name_vi
  - action_nao_say
* inform_dance_name{"lang":"vi"}
  - action_nao_dance_song_check
  - slot{"dance_null":"False", "dance_in_list":"False"}
  - utter_song_dance_not_in_list_vi
  - action_nao_say
* affirm{"lang":"vi"}
  - utter_affirm_vi
  - action_nao_say
  - action_random_dance
* deny{"lang":"vi"}
  - utter_deny_vi
  - action_nao_say

<!-- song in list -->
## ask_entertaiment_song_0_vi
* inform_song_name{"lang":"vi"}
  - action_nao_dance_song_check
  - slot{"song_null":"False", "song_in_list":"True"}
  - utter_inform_song_name_vi
  - action_nao_say
  - action_nao_sing

## ask_entertaiment_song_1_vi
* ask_entertaiment{"lang":"vi"}
  - action_nao_dance_song_check
  - slot{"song_null":"False", "song_in_list":"True"}
  - utter_inform_song_name_vi
  - action_nao_say
  - action_nao_sing

## ask_entertaiment_song_2_vi
* ask_entertaiment{"lang":"vi"}
  - action_nao_dance_song_check
  - slot{"song_null":"True"}
  - utter_ask_song_name_vi
  - action_nao_say
* inform_song_name{"lang":"vi"}
  - action_nao_dance_song_check
  - slot{"song_null":"False", "song_in_list":"True"}
  - utter_inform_song_name_vi
  - action_nao_say
  - action_nao_sing

<!-- song not in list -->
## ask_entertaiment_song_not_0_vi
* inform_song_name{"lang":"vi"}
  - action_nao_dance_song_check
  - slot{"song_null":"False", "song_in_list":"False"}
  - utter_song_dance_not_in_list_vi
  - action_nao_say
* affirm{"lang":"vi"}
  - utter_affirm_vi
  - action_nao_say
  - action_random_song
* deny{"lang":"vi"}
  - utter_deny_vi
  - action_nao_say

## ask_entertaiment_song_not_1_vi
* ask_entertaiment{"lang":"vi"}
  - action_nao_dance_song_check
  - slot{"song_null":"False", "song_in_list":"False"}
  - utter_song_dance_not_in_list_vi
  - action_nao_say
* affirm{"lang":"vi"}
  - utter_affirm_vi
  - action_nao_say
  - action_random_song
* deny{"lang":"vi"}
  - utter_deny_vi
  - action_nao_say

## ask_entertaiment_song_not_2_vi
* ask_entertaiment{"lang":"vi"}
  - action_nao_dance_song_check
  - slot{"song_null":"True"}
  - utter_ask_song_name_vi
  - action_nao_say
* inform_song_name{"lang":"vi"}
  - action_nao_dance_song_check
  - slot{"song_null":"False", "song_in_list":"False"}
  - utter_song_dance_not_in_list_vi
  - action_nao_say
* affirm{"lang":"vi"}
  - utter_affirm_vi
  - action_nao_say
  - action_random_song
* deny{"lang":"vi"}
  - utter_deny_vi
  - action_nao_say

## single_ask_wakeup_vi
* ask_wakeup{"lang":"vi"}
  - utter_affirm_vi
  - action_nao_say
  - slot{"action":"wake"}
  - action_action

## single_ask_stop_vi
* ask_stop{"lang":"vi"}
  - utter_affirm_vi
  - action_nao_say
  - slot{"action":"stop"}
  - action_action

## single_ask_rest_vi
* ask_rest{"lang":"vi"}
  - utter_affirm_vi
  - action_nao_say
  - slot{"action":"rest"}
  - action_action

## single_ask_show_room_vi
* ask_show_room{"lang":"vi"}
  - utter_ask_show_room_vi
  - action_nao_say

## single_ask_why_named_nao_vi
* ask_why_named_nao{"lang":"vi"}
  - utter_ask_why_named_nao_vi
  - action_nao_say

## single_ask_manufactory_vi
* ask_manufactory{"lang":"vi"}
  - utter_ask_manufactory_vi
  - action_nao_say 

## single_ask_policy_vi
* ask_policy{"lang":"vi"}
  - utter_ask_policy_vi
  - action_nao_say

## single_ask_showroom_floor_vi
* ask_showroom_floor{"lang":"vi"}
  - utter_ask_showroom_floor_vi
  - action_nao_say

## single_ask_delivery_method_vi
* ask_delivery_method{"lang":"vi"}
  - utter_ask_delivery_method_vi
  - action_nao_say

## single_ask_passwifi_vi
* ask_passwifi{"lang":"vi"}
  - utter_ask_passwifi_vi
  - action_nao_say

## single_evaluate_vi
* evaluate{"lang":"vi"}
  - utter_evaluate_vi
  - action_nao_say

## single_feedback_vi
* feedback{"lang":"vi"}
  - utter_feedback_vi
  - action_nao_say

## single_ask_for_emotion_vi
* ask_for_emotion{"lang":"vi"}
  - utter_ask_for_emotion_vi
  - action_nao_say

## single_thankyou_vi
* thankyou{"lang":"vi"}
  - utter_thankyou_vi
  - action_nao_say

## single_inform_name_0_vi
* inform_name{"first_name": null, "lang":"vi"}
  - utter_greet_vi
  - action_nao_say

## single_inform_name_1_vi
* inform_name{"first_name": "hòa", "lang":"vi"}
  - utter_inform_name_vi
  - action_nao_say

## single_inform_age_vi
* inform_age{"lang":"vi"}
  - utter_inform_age_vi
  - action_nao_say

## single_inform_birth_year_vi
* inform_birth_year{"lang":"vi"}
  - utter_inform_age_vi
  - action_nao_say

## single_inform_gender_male_vi
* inform_gender{"gender": "nam", "lang":"vi"}
  - utter_inform_gender_male_vi
  - action_nao_say

## single_inform_gender_female_vi
* inform_gender{"gender": "nữ", "lang":"vi"}
  - utter_inform_gender_female_vi
  - action_nao_say

## single_ask_direction_vi
* ask_direction{"lang":"vi"}
  - utter_ask_direction_vi
  - action_nao_say