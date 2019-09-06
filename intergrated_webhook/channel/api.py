import glob, os 
from rasa.nlu.training_data import load_data
from rasa.core.domain import Domain
import re
from rasa.core.actions.action import default_action_names
from rasa.nlu.training_data.message import Message

class REMatcher(object):
    def __init__(self, matchstring):
        self.matchstring = matchstring

    def match(self,regexp):
        self.rematch = re.match(regexp, self.matchstring)
        return bool(self.rematch)

    def group(self,i):
        return self.rematch.group(i)

def get_data_path():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data')

def list_intents():
    list_intents = []
    for file in glob.glob(os.path.join(get_data_path(), "nlu_*.md")):
        input_data = load_data(file)
        list_intents = list(set(list_intents + list(input_data.intents)))
    return list_intents

def list_entities():
    list_entities = []
    for file in glob.glob(os.path.join(get_data_path(), "nlu_*.md")):
        input_data = load_data(file)
        list_entities = list(set(list_entities + list(input_data.entities)))
    return list_entities

def list_actions():
    domain = Domain([], [], [], {}, [],[]).load(os.path.join(get_data_path(), "..", "domain.yml"))
    result = {
        "default" : default_action_names(),
        "custom": []
    }
    for action in domain.user_actions:
        mRe = REMatcher(action)
        if mRe.match(r"utter_\w+_(vi|ja|en)"): 
            lang = mRe.group(1) 
            if lang not in result:
                result[lang] = []
            result[lang].append(action) 
        else:
            result["custom"].append(action) 
    return result

def list_utter_msgs(utter_name):
    domain = Domain([], [], [], {}, [],[]).load(os.path.join(get_data_path(), "..", "domain.yml"))
    return domain.templates[utter_name]

def read_stories(stories_file_path):
    with open(stories_file_path, 'r', encoding='utf8') as f:
        string = f.read()
        result = []
        stories = re.findall("## (.*)\n((?:\* .*\n(?:  - .*(?:\n|$))+)+)", string)
        for story in stories:
            name, content = story
            result.append(
                {
                    "name": name,
                    "content": content
                }
            )
        return result

def list_stories():
    result = {
        "default" : []
    }
    for file in glob.glob(os.path.join(get_data_path(), "stories_*.md")):
        mRe = REMatcher(file)
        if mRe.match(r".*/stories_(vi|ja|en).md$"): 
            lang = mRe.group(1) 
            if lang not in result:
                result[lang] = read_stories(file)
        else:
            result["default"] = read_stories(file)
    return result

def update_nlu(json):
    new_intent  = json["intent_new"]
    lang_new    = json["lang_new"]
    old_intent  = json["intent_old"]
    lang_old    = json["lang_old"]
    text        = json["text"]

    # Delete text from old intent if existed
    if old_intent != "" and lang_old != "":
        input_data_old = os.path.join(get_data_path(), "nlu_%s.md" % (lang_old))
        input_data = load_data(input_data_old)
        if Message(text, {'intent': old_intent}) in input_data.training_examples:
            input_data.training_examples.remove(Message(text, {'intent': old_intent}))
        with open(input_data_old,'w') as f:
            f.write(input_data.as_markdown())

    # Append text from new intent
    input_data_new = os.path.join(get_data_path(), "nlu_%s.md" % (lang_new))
    input_data = load_data(input_data_new)
    if Message(text, {'intent': new_intent}) not in input_data.training_examples:
        new_slot = sorted(json["entities"], key = lambda x: x["start"])
        for s in new_slot[::-1]:
            t = text[s["start"]:s["end"]+1]
            text = text.replace(t, "[" + t + "](" + s["entity"] + ")",1)
        input_data.training_examples.append(Message(text, {'intent': new_intent}))
    with open(input_data_new,'w') as f:
        f.write(input_data.as_markdown())

    result = {
        "intents" : list_intents(),
        "entities" : list_entities()
    }
    return result