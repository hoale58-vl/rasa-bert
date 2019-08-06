from rasa.nlu.training_data import load_data
import json
import MeCab

input_training_file = './nlu.md'
output_training_file = './output.md'
output_intent_vocab = './vocab.class'
output_tag_vocab = './vocab.tag'
json_data = './json_data.json'

tagger = MeCab.Tagger()

def mecab_tokenize(tagger, text):
	parsed = tagger.parse(text)
	# parsed returns token => POS separated by tab in multiple lines
	x = (parsed.replace('\n', '\t').split('\t'))
	words = []
	for i in range(0, len(x) - 2, 2):
		w = x[i]
		words.append(w)
	return words

def tokenizer(tagger, text):
	return mecab_tokenize(tagger, text)

input_data = load_data(input_training_file)

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
	tokenize = tokenizer(tagger, text)
	slot = []
	intent = []
	for sl in tokenize:
		slot.append(len(list_entities))
	textTokenized = "".join(tokenize)
	if 'entities' in example.data:
		for entity in example.data['entities']:
			entity_position = -1

			if entity['value'] == text[entity['start']:entity['end']]:
				tmp = len(tokenizer(tagger, textTokenized[entity['start']:entity['end']])) # tmp = 3
				entity_position = len(tokenizer(tagger, textTokenized[0:entity['end']])) - 1 # entity_position = 3
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
	tokenize = tokenizer(tagger, text)
	slot = []
	intent = []
	for sl in tokenize:
		slot.append(len(list_entities))
	textTokenized = "".join(tokenize)
	if 'entities' in example.data:
		for entity in example.data['entities']:
			entity_position = -1
			if entity['value'] == text[entity['start']:entity['end']]:
				tmp = len(tokenizer(tagger, textTokenized[entity['start']:entity['end']]))
				entity_position = len(tokenizer(tagger, textTokenized[0:entity['end']])) - 1
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
with open(json_data, 'w') as f:
	json.dump(data, f)
