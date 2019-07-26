from rasa_nlu.training_data import load_data

input_training_file = '/home/black/workSpace/nlu/rasa_projects/vi/train_test_split/training_data.md'
output_md_file = '/home/black/workSpace/nlu/rasa-bert-finetune/data/rasa_dataset_training.json'

with open(output_md_file,'w') as f:
    f.write(load_data(input_training_file).as_json())

input_test_file = '/home/black/workSpace/nlu/rasa_projects/vi/train_test_split/test_data.md'
output_md_file = '/home/black/workSpace/nlu/rasa-bert-finetune/data/rasa_dataset_testing.json'

with open(output_md_file,'w') as f:
    f.write(load_data(input_test_file).as_json())
