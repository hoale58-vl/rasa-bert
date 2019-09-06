

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from websocket import create_connection
from rasa_sdk.events import SlotSet
from googletrans import Translator

wsControlUrl = "ws://127.0.0.1/controlbot/"

class ActionNaoDanceCheck(Action):
    def name(self) -> Text:
        return "action_nao_dance_check"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('dance_name') not in domain['slots']['dance_name']['values']:
            return [
                SlotSet("action", None), 
                SlotSet("dance_name", None), 
                SlotSet("song_name", None), 
                SlotSet("dance_in_list", "False"),
                SlotSet("song_in_list", None)
            ]
        else:
            return [
                SlotSet("action", None), 
                SlotSet("song_name", None), 
                SlotSet("dance_in_list", "True"),
                SlotSet("song_in_list", None)
            ]

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

class ActionNaoSingCheck(Action):
    def name(self) -> Text:
        return "action_nao_song_check"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_slot('song_name') not in domain['slots']['song_name']['values']:
            return [
                SlotSet("action", None), 
                SlotSet("dance_name", None), 
                SlotSet("song_name", None), 
                SlotSet("dance_in_list", None),
                SlotSet("song_in_list", "False")
            ]
        else:
            return [
                SlotSet("action", None), 
                SlotSet("dance_name", None), 
                SlotSet("dance_in_list", None),
                SlotSet("song_in_list", "True")
            ]


class ActionNaoSing(Action):
    def name(self) -> Text:
        return "action_nao_sing"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        song_name = tracker.get_slot('song_name')
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

    def translate(self, text):
        self.translator = Translator()
        return self.translator.translate(text, src='vi', dest='en').text

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            current_state = tracker.current_state()
            user_message = current_state.get('latest_message', None) 
            latest_action = current_state.get('latest_action_name', None)
            botRes = self.botRes(tracker)

            lang = user_message.get("lang", "")
            if lang == "vi":
                wsControl = create_connection(wsControlUrl)
                wsControl.send("speak::::vi::::rasa/" + latest_action + "_::::" + botRes)
                wsControl.close()
            else:
                wsControl = create_connection(wsControlUrl)
                botRes = self.translate(botRes)
                wsControl.send("speak::::en::::" + botRes)
                wsControl.close()

        except Exception as e:
            print (e)

        return []