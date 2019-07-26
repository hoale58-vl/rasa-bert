import json

input_training_file = '/home/black/workSpace/nlu/rasa_projects/data/web_software.json'
output_training_file = '/home/black/workSpace/nlu/rasa_projects/data/web_software2.json'

with open(input_training_file) as json_file:  
    data = json.load(json_file)
    for example in data['rasa_nlu_data']['common_examples']:
        for entity in example['entities']:
            start = example['text'].index(entity['value'])
            end = start + len(entity['value'])
            entity['start'] = start
            entity['end'] = end

    with open(output_training_file,'w') as outfile:
        json.dump(data, outfile, indent=4)