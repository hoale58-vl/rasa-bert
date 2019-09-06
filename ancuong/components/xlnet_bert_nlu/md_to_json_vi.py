from rasa.nlu.training_data import load_data
from CocCocTokenizer import PyTokenizer
import json
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

T = PyTokenizer(load_nontone_data=True)


def augmentation_from_lookup(input_training_file):
	import re
	input_file = open(input_training_file, 'r')
	data = input_file.read()
	input_file.close()
	matches = re.findall("(## lookup:(.*)\n(?:- (.*)\n)+)", data)
	for match in matches:
		org = match[1]
		lookups = re.findall("- (.*)\n", match[0])
		train_lines_with_org = re.findall("- .*\[" + org + "\]\(.*\).*\n", data)
		for train_line_with_org in train_lines_with_org:
			replacement = train_line_with_org
			for lookup in lookups:
				replacement = replacement + train_line_with_org.replace("[" + org + "]", "[" + lookup + "]")
			
			data = data.replace(train_line_with_org, replacement)
	output_file = open(output_training_file, 'w')
	with open(output_training_file, 'w') as output_file:
		output_file.write(data)

def tokenizer(text):
	# return text.split()
	return T.word_tokenize(text, tokenize_option=0)

def run(input_data,
		output_training_file = dir_path + '/data/output.md',
		output_intent_vocab = dir_path + '/data/vocab.class',
		output_tag_vocab = dir_path + '/data/vocab.tag'):
	# augmentation_from_lookup(input_training_file)
	# input_data = load_data(output_training_file)


	# Create vocab
	list_intents = list(input_data.intents)
	with open(output_intent_vocab, 'w') as f:
		for intent in list_intents:
			f.write("%s\n" % intent)

	list_entities = []
	for entity in list(input_data.entities):
		list_entities.append('B-' + entity)
		list_entities.append('I-' + entity)

	with open(output_tag_vocab, 'w') as f:
		for entity in list_entities:
			f.write("%s\n" % entity)
		f.write("O\n")

	# Split
	train_data, test_data = input_data.train_test_split()
	# Train data
	train_feats = []
	train_tags = []
	train_class = []
	for example in train_data.intent_examples:
		text = example.text.lower()
		tokenize = tokenizer(text)
		slot = []
		intent = []
		for sl in tokenize:
			slot.append(len(list_entities))
		textTokenized = " ".join(tokenize)
		if 'entities' in example.data:
			for entity in example.data['entities']:
				entity_position = -1

				if entity['value'] == text[entity['start']:entity['end']]:
					tmp = len(textTokenized[entity['start']:entity['end']].split()) # tmp = 3
					entity_position = len(textTokenized[0:entity['end']].split()) - 1 # entity_position = 3
				if entity_position != -1:
					while(tmp != 0):
						if tmp == 1:
							slot[entity_position] = list_entities.index('B-' + entity['entity'])
						else:
							slot[entity_position] = list_entities.index('I-' + entity['entity'])
						entity_position -= 1
						tmp -= 1

		train_feats.append(tokenize)
		train_tags.append(slot)
		train_class.append(list_intents.index(example.data['intent']))

	# Test data
	test_feats = []
	test_tags = []
	test_class = []
	for example in test_data.intent_examples:
		text = example.text.lower()
		tokenize = tokenizer(text)
		slot = []
		intent = []
		for sl in tokenize:
			slot.append(len(list_entities))
		textTokenized = " ".join(tokenize)
		if 'entities' in example.data:
			for entity in example.data['entities']:
				entity_position = -1
				if entity['value'] == text[entity['start']:entity['end']]:
					tmp = len(textTokenized[entity['start']:entity['end']].split())
					entity_position = len(textTokenized[0:entity['end']].split()) - 1
				if entity_position != -1:
					while(tmp != 0):
						if tmp == 1:
							slot[entity_position] = list_entities.index('B-' + entity['entity'])
						else:
							slot[entity_position] = list_entities.index('I-' + entity['entity'])
						entity_position -= 1
						tmp -= 1

		test_feats.append(tokenize)
		test_tags.append(slot)
		test_class.append(list_intents.index(example.data['intent']))

	data = {
		'train_feats':train_feats,
		'train_tags':train_tags,
		'train_class':train_class,
		'test_feats':test_feats,
		'test_tags':test_tags,
		'test_class':test_class
	}
	list_entities.append('O')
	return list_intents, list_entities, data

if __name__ == '__main__':
	input_training_file = dir_path + '/data/nlu_vi.md'
	input_data = load_data(input_training_file) # rasa.nlu.training_data.training_data.TrainingData
	list_intents, list_entities, data = run(input_data)
	json_data = dir_path + '/data/json_data.json'
	with open(json_data, 'w') as f:
		json.dump(data, f)
