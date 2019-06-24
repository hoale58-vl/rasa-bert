# Split train and test dataset
rasa data split nlu

# Convert data md to json
python convert_md2json.py

# Start bert service server
bert-serving-start -model_dir cased_L-12_H-768_A-12/ -num_worker=4

# Fine tune bert model with rasa dataset
https://github.com/GaoQ1/rasa-bert-finetune/
- Change model dir name in run.sh file
- Edit flag bert-service for training
mkdir data
sh run.sh

cd /home/black/workSpace/nlu/rasa-bert-finetune/rasa_model_output/
ln -sf model.ckpt-1.data-00000-of-00001 bert_model.ckpt.data-00000-of-00001
ln -sf model.ckpt-1.index bert_model.ckpt.index
ln -sf model.ckpt-1.meta bert_model.ckpt.meta

# Restart bert service server with finetune model
bert-serving-start -model_dir cased_L-12_H-768_A-12/ -num_worker=4 -tuned_model_dir /home/black/workSpace/nlu/rasa-bert-finetune/rasa_model_output/

# Get bert source feature 
pip install rasa-nlu-gao
- Add Feature to pipeline
rasa_nlu_gao.featurizers.bert_vectors_featurizer
- Add Classifier to pipeline
rasa_nlu_gao.featurizers.intent_classifier_tensorflow_embedding_bert

# Sample pipeline for chinese
language: "zh"
pipeline:
- name: "tokenizer_jieba"
- name: "bert_vectors_featurizer"
  ip: '172.16.10.46'
  port: 6555
  port_out: 6556
  show_server_config: True
  timeout: 10000
- name: "intent_classifier_tensorflow_embedding_bert"
- name: "ner_crf"
- name: "jieba_pseg_extractor"



# Gen dataset
https://github.com/SimGus/Chatette
https://github.com/snipsco/nlu-benchmark/tree/master/2018-01-Braun-et-al-extension