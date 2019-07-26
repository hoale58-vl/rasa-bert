from rasa_nlu.training_data import load_data
from CocCocTokenizer import PyTokenizer
import json

T = PyTokenizer(load_nontone_data=True)
input_training_file = './input.md'
output_intent_vocab = './vocab.class'
output_tag_vocab = './vocab.tag'
json_data = './json_data.json'

def tokenizer(text):
	# return text.split()
	return T.word_tokenize(text, tokenize_option=0)


input_data = load_data(input_training_file)

# Create vocab
list_intents = list(input_data.intents)
with open(output_intent_vocab, 'w') as f:
	for intent in list_intents:
		f.write("%s\n" % intent)

list_entities = list(input_data.entities)
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
	if 'entities' in example.data:
		for entity in example.data['entities']:
			entity_position = -1

			if entity['value'] == text[entity['start']:entity['end']]:
				entity_position = len(tokenizer(text[0:entity['end']])) - 1
			if entity_position != -1:
				slot[entity_position] = list_entities.index(entity['entity']) # Include unk and pad

			# if entity['value'] == text[entity['start']:entity['end']]:
			# 	tmp = len(text[entity['start']:entity['end']].split())
			# 	entity_position = len(tokenizer(text[0:entity['end']])) - 1

			# if entity_position != -1:
			# 	while(tmp != 0):
			# 		slot[entity_position] = list_entities.index(entity['entity'])
			# 		entity_position -= 1
			# 		tmp -= 1
			# 	slot[entity_position] += 2 # Include unk and pad

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
	if 'entities' in example.data:
		for entity in example.data['entities']:
			entity_position = -1

			if entity['value'] == text[entity['start']:entity['end']]:
				entity_position = len(tokenizer(text[0:entity['end']])) - 1
			if entity_position != -1:
				slot[entity_position] = list_entities.index(entity['entity'])

			# if entity['value'] == text[entity['start']:entity['end']]:
			# 	tmp = len(text[entity['start']:entity['end']].split())
			# 	entity_position = len(tokenizer(text[0:entity['end']])) - 1

			# if entity_position != -1:
			# 	while(tmp != 0):
			# 		slot[entity_position] = list_entities.index(entity['entity'])
			# 		entity_position -= 1
			# 		tmp -= 1
			# 		slot[entity_position] += 2 # Include unk and pad

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
with open(json_data, 'w') as f:
	json.dump(data, f)