from rasa_nlu.training_data import load_data

input_training_file = './training_data.json'
output_md_file = './training_data.md'

with open(output_md_file,'w') as f:
    f.write(load_data(input_training_file).as_markdown())

