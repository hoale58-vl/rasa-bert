# Prepare
cd components/xlnet_nlu/lib
git clone https://github.com/sz128/slot_filling_and_intent_detection_of_SLU/
mv slot_filling_and_intent_detection_of_SLU/* .
rm -rf slot_filling_and_intent_detection_of_SLU
pip install pytorch_transformers

# Bug in rasa slack api
- Allow scope chat:write:bot and channels:read in app permissions
- Change as_user from True to False
- Change channel -> list
- Directory path:  /home/black/anaconda3/envs/rasa_chatbot/lib/python3.6/site-packages/rasa/core/channels/slack.py
- New source in edited directory

# Download model


# Tracker store
pip install pymysql

# Mecab - Japanese tokenizer
pip install mecab-python3