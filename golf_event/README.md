pip install watchdog

# Modified on Distil bert
models/slot_tagger.py -> 101 Line
- DistilBert doesn't have `token_type_ids`, you don't need to indicate which token belongs to which segment. Just separate your segments with the separation token `tokenizer.sep_token` (or `[SEP]`)
- DistilBert doesn't have options to select the input positions (`position_ids` input). This could be added if necessary though, just let's us know if you need this option.
https://github.com/huggingface/pytorch-transformers/blob/master/pytorch_transformers/modeling_distilbert.py
https://github.com/sz128/slot_filling_and_intent_detection_of_SLU/blob/master/models/slot_tagger.py
https://github.com/huggingface/pytorch-transformers/blob/master/pytorch_transformers/modeling_bert.py
