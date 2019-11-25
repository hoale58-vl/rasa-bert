from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from websocket import create_connection
from rasa_sdk.events import SlotSet
import random

wsControlUrl = "ws://127.0.0.1/controlbot/"

class ActionNaoDance(Action):
    def name(self) -> Text:
        return "action_nao_dance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dance_name = tracker.get_slot('dance_name')

        try:
            wsControl = create_connection(wsControlUrl)
            wsControl.send("motion::::dance::::" + dance_name)
            wsControl.close()
        except Exception as e:
            print (e)

        return [
                SlotSet("action", None), 
                SlotSet("dance_name", None), 
                SlotSet("song_name", None), 
                SlotSet("dance_in_list", None),
                SlotSet("song_in_list", None)
            ]

class ActionRandomDance(Action):
    def name(self) -> Text:
        return "action_random_dance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dance_name = random.choice(domain['slots']['dance_name']['values'])

        try:
            wsControl = create_connection(wsControlUrl)
            wsControl.send("motion::::dance::::" + dance_name)
            wsControl.close()
        except Exception as e:
            print (e)

        return [
                SlotSet("action", None), 
                SlotSet("dance_name", None), 
                SlotSet("song_name", None), 
                SlotSet("dance_in_list", None),
                SlotSet("song_in_list", None)
            ]

class ActionNaoDanceSongCheck(Action):
    def name(self) -> Text:
        return "action_nao_dance_song_check"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        action = None
        dance_name = None
        song_name = None
        dance_in_list = None
        song_in_list = None
        song_null = None
        dance_null = None

        if tracker.get_slot('dance_name') is not None:
            if tracker.get_slot('dance_name') not in domain['slots']['dance_name']['values']:
                dance_in_list = "False"
                dance_null = "False"
            else:
                dance_in_list = "True"
                dance_null = "False"
                dance_name = tracker.get_slot('dance_name')
        elif tracker.get_slot('song_name') is not None:
            if tracker.get_slot('song_name') not in domain['slots']['song_name']['values']:
                song_in_list = "False"
                song_null = "False"
            else:
                song_in_list = "True"
                song_null = "False"
                song_name = tracker.get_slot('song_name')
        elif tracker.get_slot('dance_name') is None:
            dance_null = True
        elif tracker.get_slot('song_name') is None:
            song_null = True

        return [
                SlotSet("action", action),
                SlotSet("dance_name", dance_name), 
                SlotSet("song_name", song_name), 
                SlotSet("dance_in_list", dance_in_list),
                SlotSet("song_in_list", song_in_list),
                SlotSet("song_null", song_null),
                SlotSet("dance_null", song_null),
            ]

class ActionNaoSing(Action):
    def name(self) -> Text:
        return "action_nao_sing"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        song_name = tracker.get_slot('song_name')
        list_guitar = [
            "vẽ",
            "người ta nói",
            "gió vẫn hát",
            "có chàng_trai viết lên cây",
            "trọn tình",
            "lớn rồi còn khóc_nhè"
        ]
        guitar = ""
        if song_name in list_guitar:
            guitar = "guitar"

        try:
            wsControl = create_connection(wsControlUrl)
            wsControl.send("speak::::sing::::song/" + song_name + ".mp3" + "::::" + guitar)
            wsControl.close()
        except Exception as e:
            print (e)

        return [
                SlotSet("action", None), 
                SlotSet("dance_name", None), 
                SlotSet("song_name", None), 
                SlotSet("dance_in_list", None),
                SlotSet("song_in_list", None)
            ]

class ActionRandomSong(Action):
    def name(self) -> Text:
        return "action_random_song"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        song_name = random.choice(domain['slots']['song_name']['values'])
        try:
            wsControl = create_connection(wsControlUrl)
            wsControl.send("speak::::sing::::song/" + song_name + ".mp3")
            wsControl.close()
        except Exception as e:
            print (e)

        return [
                SlotSet("action", None), 
                SlotSet("dance_name", None), 
                SlotSet("song_name", None), 
                SlotSet("dance_in_list", None),
                SlotSet("song_in_list", None)
            ]

class ActionNaoSay(Action):
    def name(self) -> Text:
        return "action_nao_say"

    def botRes(self, tracker):
        botRes = "..."
        for event in tracker.events:
            if (event.get("event") == "bot") and (event.get("event") is not None):
                botRes = event.get("text")
        return botRes

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            current_state = tracker.current_state()
            user_message = current_state.get('latest_message', None) 
            latest_action = current_state.get('latest_action_name', None)
            botRes = self.botRes(tracker)

            lang = user_message.get("lang", "")
            print(lang)
            print(botRes)
            print(tracker.get_slot('lang'))
            if lang == "vi":
                wsControl = create_connection(wsControlUrl)
                wsControl.send("speak::::vi::::rasa/" + latest_action + "_::::" + botRes)
                wsControl.close()
            else:
                wsControl = create_connection(wsControlUrl)
                wsControl.send("speak::::en::::" + botRes)
                wsControl.close()

        except Exception as e:
            print (e)

        return []

class ActionAction(Action):
    def name(self) -> Text:
        return "action_action"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        action = tracker.get_slot('action')

        try:
            wsControl = create_connection(wsControlUrl)
            if action == "rest":
                wsControl.send("motion::::wake::::down")
            elif action == "wake":
                wsControl.send("motion::::wake::::up")
            elif action == "stop":
                wsControl.send("motion::::stopall::::stop")
            wsControl.close()
        except Exception as e:
            print (e)

        return [
                SlotSet("action", None), 
            ]

class ActionMode(Action):
    def name(self) -> Text:
        return "action_mode"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        mode_action = tracker.get_slot('mode_action')
        mode = tracker.get_slot('mode')

        try:
            wsControl = create_connection(wsControlUrl)
            if mode_action == "bật":
                if mode == 'giọng_nói':
                    wsControl.send("mode::::sound::::start")
                elif mode == 'micro':
                    wsControl.send("micro::::start::::start")
                elif mode == 'camera':
                    wsControl.send("gstream::::start::::640,480,15,0")
            elif mode_action == "tắt":
                if mode == 'giọng_nói':
                    wsControl.send("mode::::sound::::stop")
                elif mode == 'micro':
                    wsControl.send("micro::::stop::::stop")
                elif mode == 'camera':
                    wsControl.send("gstream::::stop::::stop")
            wsControl.close()
        except Exception as e:
            print (e)

        return [
                SlotSet("mode_action", None), 
                SlotSet("mode", None), 
            ]