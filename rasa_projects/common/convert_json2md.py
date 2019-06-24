from rasa_nlu.training_data import load_data

input_training_file = '/home/black/workSpace/nlu/rasa_projects/data/web_software2.json'
output_md_file = '/home/black/workSpace/nlu/rasa_projects/data/web_software2.md'

with open(output_md_file,'w') as f:
    f.write(load_data(input_training_file).as_markdown())

