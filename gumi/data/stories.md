## single_pad
* <pad>
  - utter_pad
  - action_nao_say

## single_unk
* <unk>
  - utter_unk
  - action_nao_say

## single_ask_do_something
* ask_do_something
  - utter_ask_do_something
  - action_nao_say

## ask_entertaiment_dance_0
* ask_entertaiment{"action": "nhảy"} OR ask_entertaiment{"action": "dance"} 
  - slot{"dance_name":"gangnam style"}
  - action_nao_dance_check
  - slot{"dance_in_list":"True"}
  - action_nao_dance

## ask_entertaiment_dance_1
* ask_entertaiment{"action": "nhảy"}  OR ask_entertaiment{"action": "dance"}
  - slot{"dance_name":null}
  - utter_ask_dance_name
  - action_nao_say
* inform_dance_name{"dance_name": "gangnam style"}
  - action_nao_dance_check
  - slot{"dance_in_list":"True"}
  - action_nao_dance

## ask_entertaiment_dance_not_0
* ask_entertaiment{"action": "nhảy"} OR ask_entertaiment{"action": "dance"} 
  - slot{"dance_name":"gangnam style"}
  - action_nao_dance_check
  - slot{"dance_in_list":"False"}
  - utter_song_dance_not_in_list
  - action_nao_say
  - utter_list_dance
  - action_nao_say

## ask_entertaiment_dance_not_1
* ask_entertaiment{"action": "nhảy"}  OR ask_entertaiment{"action": "dance"}
  - slot{"dance_name":null}
  - utter_ask_dance_name
  - action_nao_say
* inform_dance_name{"dance_name": "gangnam style"}
  - action_nao_dance_check
  - slot{"dance_in_list":"False"}
  - utter_song_dance_not_in_list
  - action_nao_say
  - utter_list_dance
  - action_nao_say

## ask_entertaiment_dance_not_2
* ask_entertaiment{"action": "nhảy"} OR ask_entertaiment{"action": "dance"} 
  - slot{"song_name": "sóng gió"}
  - action_nao_dance_check
  - slot{"dance_in_list":"False"}
  - utter_song_dance_not_in_list
  - action_nao_say
  - utter_list_dance
  - action_nao_say

## ask_entertaiment_song_0
* ask_entertaiment{"action": "hát"} OR ask_entertaiment{"action": "sing"} 
  - slot{"song_name": "sóng gió"}
  - action_nao_song_check
  - slot{"song_in_list":"True"}
  - action_nao_sing

## ask_entertaiment_song_1
* ask_entertaiment{"action": "hát"} OR ask_entertaiment{"action": "sing"} 
  - slot{"song_name": null}
  - utter_ask_song_name
  - action_nao_say
* inform_song_name{"song_name": "sóng gió"}
  - action_nao_song_check
  - slot{"song_in_list":"True"}
  - action_nao_sing

## ask_entertaiment_song_not_0
* ask_entertaiment{"action": "hát"} OR ask_entertaiment{"action": "sing"} 
  - slot{"song_name": "sóng gió"}
  - action_nao_song_check
  - slot{"song_in_list":"False"}
  - utter_song_dance_not_in_list
  - action_nao_say
  - utter_list_song
  - action_nao_say

## ask_entertaiment_song_not_1
* ask_entertaiment{"action": "hát"} OR ask_entertaiment{"action": "sing"} 
  - slot{"song_name": null}
  - utter_ask_song_name
  - action_nao_say
* inform_song_name{"song_name": "sóng gió"}
  - action_nao_song_check
  - slot{"song_in_list":"False"}
  - utter_song_dance_not_in_list
  - action_nao_say
  - utter_list_song
  - action_nao_say

## ask_entertaiment_song_not_2
* ask_entertaiment{"action": "hát"} OR ask_entertaiment{"action": "sing"} 
  - slot{"dance_name": "gangnam style"}
  - action_nao_song_check
  - slot{"song_in_list":"False"}
  - utter_song_dance_not_in_list
  - action_nao_say
  - utter_list_song
  - action_nao_say

## single_greet
* greet
  - utter_greet
  - action_nao_say

## single_intro_company
* intro_company
  - utter_intro_company
  - action_nao_say

## single_rude
* rude
  - utter_rude
  - action_nao_say

## single_deny
* deny
  - utter_deny
  - action_nao_say

## single_bye
* bye
  - utter_bye
  - action_nao_say

## single_product_company
* product_company
  - utter_product_company
  - action_nao_say

## single_ask_talk_real_person_0
* ask_talk_real_person{"position": null, "dest": null}
  - utter_ask_talk_real_person
  - action_nao_say

## single_ask_talk_real_person_1
* ask_talk_real_person{"position": null, "dest": "nhân sự"}
  - utter_ask_talk_real_person_1
  - action_nao_say

## single_ask_talk_real_person_2
* ask_talk_real_person{"dest": null, "position": "giám đốc"}
  - utter_ask_talk_real_person_2
  - action_nao_say

## single_ask_talk_real_person_3
* ask_talk_real_person{"dest": "nhân sự", "position": "giám đốc"}
  - utter_ask_talk_real_person_3
  - action_nao_say

## single_ask_for_health
* ask_for_health
  - utter_ask_for_health
  - action_nao_say

## single_ask_bot_infor
* ask_bot_infor
  - utter_ask_bot_infor
  - action_nao_say

## single_ask_country
* ask_country
  - utter_ask_country
  - action_nao_say

## single_phone_company
* phone_company
  - utter_phone_company
  - action_nao_say

## single_ask_ai_feature
* ask_ai_feature
  - utter_ask_ai_feature
  - action_nao_say

## single_ask_name
* ask_name
  - utter_ask_name
  - action_nao_say

## single_scale_company
* scale_company
  - utter_scale_company
  - action_nao_say

## single_working_hours_company
* working_hours_company
  - utter_working_hours_company
  - action_nao_say

## single_ask_for_help
* ask_for_help
  - utter_ask_for_help
  - action_nao_say

## single_affirm
* affirm
  - utter_affirm
  - action_nao_say

## single_ask_for_humor
* ask_for_humor
  - utter_ask_for_humor
  - action_nao_say

## single_mood_great
* mood_great
  - utter_mood_great
  - action_nao_say

## single_evaluate
* evaluate{"rate": null}
  - utter_evaluate
  - action_nao_say

## single_evaluate_1
* evaluate{"rate": "ngu"}
  - utter_evaluate_1
  - action_nao_say

## single_ask_for_emotion
* ask_for_emotion
  - utter_ask_for_emotion
  - action_nao_say

## single_thankyou
* thankyou
  - utter_thankyou
  - action_nao_say

## single_mood_unhappy
* mood_unhappy
  - utter_mood_unhappy
  - action_nao_say

## single_location_company
* location_company
  - utter_location_company
  - action_nao_say

## single_inform_name_0
* inform_name{"first_name": null}
  - utter_greet
  - action_nao_say

## single_inform_name_1
* inform_name{"first_name": "hòa"}
  - utter_inform_name
  - action_nao_say

## single_inform_age
* inform_age
  - utter_inform_age
  - action_nao_say

## single_inform_gender_male
* inform_gender{"gender": "nam"} OR inform_gender{"gender": "male"}
  - utter_inform_gender_male
  - action_nao_say

## single_inform_gender_female
* inform_gender{"gender": "nữ"} OR inform_gender{"gender": "female"}
  - utter_inform_gender_female
  - action_nao_say

## single_ask_direction
* ask_direction
  - utter_ask_direction
  - action_nao_say

