import argparse
import random
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import os, sys, time
import logging
import gc

sys.path.append('.')
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

from pytorch_transformers import BertTokenizer, BertModel, XLNetTokenizer, XLNetModel  , DistilBertTokenizer, DistilBertModel
from pytorch_transformers.optimization import AdamW, WarmupLinearSchedule
from models.optimization import BertAdam
from utils.bert_xlnet_inputs import prepare_inputs_for_bert_xlnet

import models.slot_tagger as slot_tagger
import models.slot_tagger_with_focus as slot_tagger_with_focus
import models.slot_tagger_crf as slot_tagger_with_crf
import models.snt_classifier as snt_classifier

import utils.vocab_reader as vocab_reader
import utils.data_reader_for_elmo as data_reader
import utils.read_wordEmb as read_wordEmb
import utils.util as util
import utils.acc as acc

from .md_to_json_en import run as run_en
from .md_to_json_vi import run as run_vi
from .md_to_json_ja import run as run_ja

MODEL_CLASSES = {
        'bert': (BertModel, BertTokenizer),
        'xlnet': (XLNetModel, XLNetTokenizer),
        'distil-bert': (DistilBertModel, DistilBertTokenizer)
        }

class LoadData(object):
    def __init__(self, data, train=True):
        self.feats =  {}
        self.tags = {}
        self.intent = {}
        self.fromJson(data, train)

    def fromJson(self, data, train):
        if train:
            for key, val in enumerate(data['train_tags']):
                data['train_tags'][key] = [x+2 for x in val]
                data['train_class'][key] += 2
            self.feats['data'] = data['train_feats']
            self.tags['data'] = data['train_tags']
            self.intent['data'] = data['train_class']
        else:
            for key, val in enumerate(data['test_tags']):
                data['test_tags'][key] = [x+2 for x in val]
                data['test_class'][key] += 2
            self.feats['data'] = data['test_feats']
            self.tags['data'] = data['test_tags']
            self.intent['data'] = data['test_class']

class TrainParam(object):
    def __init__(self, lang):
        self.setParam(lang)
        self.validateParam()

    def setParam(self, lang):
        self.task_st = 'slot_tagger' # slot_tagger, slot_tagger_with_crf, slot_tagger_with_focus
        self.task_sc = 'hiddenAttention' # none, hiddenAttention, hiddenCNN, maxPooling, 2tails 
        self.bidirectional = True
        self.lr = 1e-5 # 1e-5, 5e-5, 1e-4, 1e-3 
        self.dropout = 0.1 # 0.1, 0.5 
        self.batchSize = 32 # 16, 32 
        self.experiment = "exp" 
        self.deviceId = 0 # 0, -1
        self.optimizer_sel='bertadam' # adam, bertadam
        #max_norm_of_gradient_clip=5
        self.max_epoch = 50 
        self.hidden_size = 100 # 100, 200 
        self.num_layers = 1
        self.tag_emb_size = 100  ## for slot_tagger_with_focus 
        self.st_weight = 0.5
        self.pretrained_model_type = "distil-bert" # bert, xlnet, distil-bert
        self.fix_pretrained_model = False
        #####################
        # bert-base-uncased, 
        # bert-large-uncased, 
        # bert-base-cased, 
        # bert-large-cased, 
        # bert-base-multilingual-uncased, 
        # bert-base-multilingual-cased, 
        # bert-base-chinese
        # xlnet-base-cased
        # xlnet-large-cased
        # distilbert-base-uncased
        #####################
        # if lang in ['vi', 'en']:
        #     self.pretrained_model_name = "bert-base-uncased"
        # else:
        #     self.pretrained_model_name = "bert-base-multilingual-uncased"
        self.pretrained_model_name = 'distilbert-base-uncased'
        
        self.sc_type ='single_cls_CE' # single_cls_CE , multi_cls_BCE
        self.random_seed = 999
        self.save_vocab = 'vocab'
        self.out_path = os.path.join(os.path.dirname(__file__), "model", lang)
        self.fix_bert_model = None
        self.warmup_proportion=0.1
        self.max_norm = 5
        self.save_model_file_name='model'
        self.init_weight = 0.2

        if self.sc_type == 'multi_cls_BCE':
            self.multiClass = True
        else:
            self.multiClass = False
        if self.task_st == 'slot_tagger_with_focus':
            self.enc_dec, self.crf = True, False
        elif self.task_st == 'slot_tagger_with_crf':
            self.enc_dec, self.crf = False, True
        else:
            self.enc_dec, self.crf = False, False
            
        if self.st_weight == 1 or self.task_sc == 'none':
            self.task_sc = None

    def validateParam(self):
        assert self.task_st in {'slot_tagger', 'slot_tagger_with_focus', 'slot_tagger_with_crf'}
        assert self.task_sc in {'none', '2tails', 'maxPooling', 'hiddenCNN', 'hiddenAttention'}
        assert self.sc_type in {'single_cls_CE', 'multi_cls_BCE'}
        assert 0 < self.st_weight <= 1


class SlotNluTrain(object):
    def __init__(self, training_data, lang="vi"):
        self.param = TrainParam(lang)
        self.outputDirectory(lang)
        self.deviceSelect()
        self.seed()
        if lang in ['vi']:
            vocab_class, vocab_tag, data = run_vi(training_data)
        elif lang in ['en']:
            vocab_class, vocab_tag, data = run_en(training_data)
        elif lang in ['ja']:
            vocab_class, vocab_tag, data = run_ja(training_data)
        else:
            raise ValueError("lang not set")

        self.loadData(data, vocab_tag, vocab_class)
        self.loadModel()
        self.lossFunction()
        self.optimizer()

    def deviceSelect(self):
        if self.param.deviceId >= 0:
            import utils.gpu_selection as gpu_selection
            if self.param.deviceId > 0:
                self.param.deviceId, gpu_name, valid_gpus = gpu_selection.auto_select_gpu(assigned_gpu_id=self.param.deviceId - 1)
            elif self.param.deviceId == 0:
                self.param.deviceId, gpu_name, valid_gpus = gpu_selection.auto_select_gpu()
            print("Valid GPU list: %s ; GPU %d (%s) is auto selected." % (valid_gpus, self.param.deviceId, gpu_name))
            torch.cuda.set_device(self.param.deviceId)
            self.device = torch.device("cuda") # is equivalent to torch.device('cuda:X') where X is the result of torch.cuda.current_device()
        else:
            print("CPU is used.")
            self.device = torch.device("cpu")

    def outputDirectory(self, lang):
        if not os.path.exists(self.param.out_path):
            os.makedirs(self.param.out_path)
        if not os.path.exists(os.path.join(self.param.out_path, lang)):
            os.makedirs(os.path.join(self.param.out_path, lang))

    def seed(self):
        random.seed(self.param.random_seed)
        torch.manual_seed(self.param.random_seed)
        np.random.seed(self.param.random_seed)

    def loadVocab(self, vocab, bos_eos=False, no_pad=False, no_unk=False, separator=':'):
        '''file format: "word : idx" '''
        word2id, id2word = {}, {}
        if not no_pad:
            word2id['<pad>'] = len(word2id)
            id2word[len(id2word)] = '<pad>'
        if not no_unk:
            word2id['<unk>'] = len(word2id)
            id2word[len(id2word)] = '<unk>'
        if bos_eos == True:
            word2id['<s>'] = len(word2id)
            id2word[len(id2word)] = '<s>'
            word2id['</s>'] = len(word2id)
            id2word[len(id2word)] = '</s>'
        for line in vocab:
            if separator in line:
                word, idx = line.strip('\r\n').split(' '+separator+' ')
                idx = int(idx)
            else:
                word = line.strip()
                idx = len(word2id)
            if word not in word2id:
                word2id[word] = idx
                id2word[idx] = word
        return word2id, id2word

    def loadData(self, data, vocab_tag, vocab_class):
        self.trainData = LoadData(data, True)
        self.validData = LoadData(data, False)
        self.tag_to_idx, self.idx_to_tag = self.loadVocab(vocab_tag, bos_eos=False)
        self.class_to_idx, self.idx_to_class = self.loadVocab(vocab_class, bos_eos=False)

        vocab_reader.save_vocab(self.idx_to_tag, os.path.join(self.param.out_path, self.param.save_vocab+'.tag'))
        vocab_reader.save_vocab(self.idx_to_class, os.path.join(self.param.out_path, self.param.save_vocab+'.class'))

    def loadModel(self):
        # Tokenize and pretrained model
        pretrained_model_class, tokenizer_class = MODEL_CLASSES[self.param.pretrained_model_type]
        self.tokenizer = tokenizer_class.from_pretrained(self.param.pretrained_model_name)
        if self.param.fix_pretrained_model:
            self.pretrained_model = pretrained_model_class.from_pretrained(self.param.pretrained_model_name, output_hidden_states = True)
        else:
            self.pretrained_model = pretrained_model_class.from_pretrained(self.param.pretrained_model_name)
        emb_size = None

        # Model tag
        if self.param.task_st == 'slot_tagger':
            self.model_tag = slot_tagger.LSTMTagger(emb_size, self.param.hidden_size, None, len(self.tag_to_idx), 
                                            bidirectional=self.param.bidirectional, 
                                            num_layers=self.param.num_layers, 
                                            dropout=self.param.dropout, 
                                            device=self.device, 
                                            pretrained_model=self.pretrained_model, 
                                            pretrained_model_type=self.param.pretrained_model_type, 
                                            fix_pretrained_model=self.param.fix_pretrained_model)
        elif self.param.task_st == 'slot_tagger_with_focus':
            self.model_tag = slot_tagger_with_focus.LSTMTagger_focus(emb_size, self.param.tag_emb_size, self.param.hidden_size, None, len(self.tag_to_idx), 
                                                bidirectional=self.param.bidirectional, 
                                                num_layers=self.param.num_layers, 
                                                dropout=self.param.dropout, 
                                                device=self.device, 
                                                pretrained_model=self.pretrained_model, 
                                                pretrained_model_type=self.param.pretrained_model_type, 
                                                fix_pretrained_model=self.param.fix_pretrained_model)
        elif self.param.task_st == 'slot_tagger_with_crf':
            self.model_tag = slot_tagger_with_crf.LSTMTagger_CRF(emb_size, self.param.hidden_size, None, len(self.tag_to_idx), 
                                                bidirectional=self.param.bidirectional, 
                                                num_layers=self.param.num_layers, 
                                                dropout=self.param.dropout, 
                                                device=self.device, 
                                                pretrained_model=self.pretrained_model, 
                                                pretrained_model_type=self.param.pretrained_model_type, 
                                                fix_pretrained_model=self.param.fix_pretrained_model)
        else:
            raise ValueError('Bad value of task_st')

        # Model classifier
        if self.param.task_sc == '2tails':
            self.model_class = snt_classifier.sntClassifier_2tails(self.param.hidden_size, len(self.class_to_idx), 
                                                              bidirectional=self.param.bidirectional, 
                                                              num_layers=self.param.num_layers, 
                                                              dropout=self.param.dropout, 
                                                              device=self.device, 
                                                              multi_class=self.param.multiClass)
            self.encoder_info_filter = lambda info: info[0]
        elif self.param.task_sc == 'maxPooling':
            self.model_class = snt_classifier.sntClassifier_hiddenPooling(self.param.hidden_size, len(self.class_to_idx), 
                                                                     bidirectional=self.param.bidirectional, 
                                                                     num_layers=self.param.num_layers, 
                                                                     dropout=self.param.dropout, 
                                                                     device=self.device, 
                                                                     multi_class=self.param.multiClass, 
                                                                     pooling='max')
            self.encoder_info_filter = lambda info: (info[1], info[2])
        elif self.param.task_sc == 'hiddenCNN':
            self.model_class = snt_classifier.sntClassifier_hiddenCNN(self.param.hidden_size, len(self.class_to_idx), 
                                                                 bidirectional=self.param.bidirectional, 
                                                                 num_layers=self.param.num_layers, 
                                                                 dropout=self.param.dropout, 
                                                                 device=self.device, 
                                                                 multi_class=self.param.multiClass)
            self.encoder_info_filter = lambda info: (info[1], info[2])
        elif self.param.task_sc == 'hiddenAttention':
            self.model_class = snt_classifier.sntClassifier_hiddenAttention(self.param.hidden_size, len(self.class_to_idx), 
                                                                       bidirectional=self.param.bidirectional, 
                                                                       num_layers=self.param.num_layers, 
                                                                       dropout=self.param.dropout, 
                                                                       device=self.device, 
                                                                       multi_class=self.param.multiClass)
            self.encoder_info_filter = lambda info: info
        else:
            raise ValueError('Bad value of task_sc')

        self.model_tag = self.model_tag.to(self.device)
        self.model_tag.init_weights(self.param.init_weight)
        if self.param.task_sc:
            self.model_class = self.model_class.to(self.device)
            self.model_class.init_weights(self.param.init_weight)

    def lossFunction(self):
        weight_mask = torch.ones(len(self.tag_to_idx), device=self.device)
        weight_mask[self.tag_to_idx['<pad>']] = 0
        self.tag_loss_function = nn.NLLLoss(weight=weight_mask, size_average=False)
        if self.param.task_sc:
            if self.param.multiClass:
                self.class_loss_function = nn.BCELoss(size_average=False)
            else:
                self.class_loss_function = nn.NLLLoss(size_average=False)

    def optimizer(self):
        # optimizer
        if self.param.optimizer_sel.lower() == 'adam':
            params = []
            params += list(self.model_tag.parameters())
            if self.param.task_sc:
                params += list(self.model_class.parameters())
            params = filter(lambda p: p.requires_grad, params)
            self.optimizer = optim.Adam(params, lr=lr, betas=(0.9, 0.999), eps=1e-8, weight_decay=0) # (beta1, beta2)
        elif self.param.optimizer_sel.lower() == 'bertadam':
            named_params = []
            named_params += list(self.model_tag.named_parameters())
            if self.param.task_sc:
                named_params += list(self.model_class.named_parameters())
            named_params = filter(lambda p: p[1].requires_grad, named_params)
            no_decay = ['bias', 'LayerNorm.bias', 'LayerNorm.weight']
            optimizer_grouped_parameters = [
                {'params': [p for n, p in named_params if not any(nd in n for nd in no_decay)], 'weight_decay': 0.01},
                {'params': [p for n, p in named_params if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
                ]
            num_train_optimization_steps = len(self.trainData.feats['data']) // self.param.batchSize * self.param.max_epoch
            self.optimizer = BertAdam(optimizer_grouped_parameters, lr=self.param.lr, warmup=self.param.warmup_proportion, t_total=num_train_optimization_steps)
        elif self.param.optimizer_sel.lower() == 'adamw':
            params = []
            params += list(self.model_tag.parameters())
            if self.param.task_sc:
                params += list(self.model_class.parameters())
            params = filter(lambda p: p.requires_grad, params)
            named_params = []
            named_params += list(self.model_tag.named_parameters())
            if self.param.task_sc:
                named_params += list(self.model_class.named_parameters())
            named_params = filter(lambda p: p[1].requires_grad, named_params)
            no_decay = ['bias', 'LayerNorm.bias', 'LayerNorm.weight']
            optimizer_grouped_parameters = [
                {'params': [p for n, p in named_params if not any(nd in n for nd in no_decay)], 'weight_decay': 0.01},
                {'params': [p for n, p in named_params if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
                ]
            num_train_optimization_steps = len(self.trainData.feats['data']) // self.param.batchSize * self.param.max_epoch
            self.optimizer = AdamW(optimizer_grouped_parameters, lr=self.param.lr, correct_bias=False)  # To reproduce BertAdam specific behavior set correct_bias=False
            self.scheduler = WarmupLinearSchedule(self.optimizer, warmup_steps=int(self.param.warmup_proportion * num_train_optimization_steps), t_total=num_train_optimization_steps)  # PyTorch scheduler
        else:
            raise ValueError('Bad value of optimizer')

    def decode(self, data_feats, data_tags, data_class, output_path):
        data_index = np.arange(len(data_feats))
        losses = []
        TP, FP, FN, TN = 0.0, 0.0, 0.0, 0.0
        TP2, FP2, FN2, TN2 = 0.0, 0.0, 0.0, 0.0
        with open(output_path, 'w') as f:
            for j in range(0, len(data_index), self.param.batchSize):
                words, tags, raw_tags, classes, raw_classes, lens = data_reader.get_minibatch_with_class(data_feats, data_tags, data_class, self.tag_to_idx, self.class_to_idx, data_index, j, 
                                                                                                            self.param.batchSize, 
                                                                                                            add_start_end=False, 
                                                                                                            multiClass=self.param.multiClass, 
                                                                                                            keep_order=False, 
                                                                                                            enc_dec_focus=self.param.enc_dec, 
                                                                                                            device=self.device)
                inputs = prepare_inputs_for_bert_xlnet(words, lens, self.tokenizer, 
                        cls_token_at_end=bool(self.param.pretrained_model_type in ['xlnet']),  # xlnet has a cls token at the end
                        cls_token=self.tokenizer.cls_token,
                        sep_token=self.tokenizer.sep_token,
                        cls_token_segment_id=2 if self.param.pretrained_model_type in ['xlnet'] else 0,
                        pad_on_left=bool(self.param.pretrained_model_type in ['xlnet']), # pad on the left for xlnet
                        pad_token_segment_id=4 if self.param.pretrained_model_type in ['xlnet'] else 0,
                        device=self.device)
    
                if self.param.enc_dec:
                    greed_decoding = True
                    if greed_decoding:
                        tag_scores_1best, outputs_1best, encoder_info = self.model_tag.decode_greed(inputs, tags[:, 0:1], lens, with_snt_classifier=True)
                        tag_loss = self.tag_loss_function(tag_scores_1best.contiguous().view(-1, len(self.tag_to_idx)), tags[:, 1:].contiguous().view(-1))
                        top_pred_slots = outputs_1best.cpu().numpy()
                    else:
                        beam_size = 2
                        beam_scores_1best, top_path_slots, encoder_info = self.model_tag.decode_beam_search(inputs, lens, beam_size, self.tag_to_idx, with_snt_classifier=True)
                        top_pred_slots = [[item[0].item() for item in seq] for seq in top_path_slots]
                        ppl = beam_scores_1best.cpu() / torch.tensor(lens, dtype=torch.float)
                        tag_loss = ppl.exp().sum()
                    #tags = tags[:, 1:].data.cpu().numpy()
                elif self.param.crf:
                    max_len = max(lens)
                    masks = [([1] * l) + ([0] * (max_len - l)) for l in lens]
                    masks = torch.tensor(masks, dtype=torch.uint8, device=self.device)
                    crf_feats, encoder_info = self.model_tag._get_lstm_features(inputs, lens, with_snt_classifier=True)
                    tag_path_scores, tag_path = self.model_tag.forward(crf_feats, masks)
                    tag_loss = self.model_tag.neg_log_likelihood(crf_feats, masks, tags)
                    top_pred_slots = tag_path.data.cpu().numpy()
                else:
                    tag_scores, encoder_info = self.model_tag(inputs, lens, with_snt_classifier=True)
                    tag_loss = self.tag_loss_function(tag_scores.contiguous().view(-1, len(self.tag_to_idx)), tags.view(-1))
                    top_pred_slots = tag_scores.data.cpu().numpy().argmax(axis=-1)
                    #tags = tags.data.cpu().numpy()

                if self.param.task_sc:
                    class_scores = self.model_class(self.encoder_info_filter(encoder_info))
                    class_loss = self.class_loss_function(class_scores, classes)
                    if self.param.multiClass:
                        snt_probs = class_scores.data.cpu().numpy()
                    else:
                        snt_probs = class_scores.data.cpu().numpy().argmax(axis=-1)
                    losses.append([tag_loss.item()/sum(lens), class_loss.item()/len(lens)])
                else:
                    losses.append([tag_loss.item()/sum(lens), 0])
    
                #classes = classes.data.cpu().numpy()
                for idx, pred_line in enumerate(top_pred_slots):
                    length = lens[idx]
                    pred_seq = [self.idx_to_tag[tag] for tag in pred_line][:length]
                    lab_seq = [self.idx_to_tag[tag] if type(tag) == int else tag for tag in raw_tags[idx]]
                    pred_chunks = acc.get_chunks(['O']+pred_seq+['O'])
                    label_chunks = acc.get_chunks(['O']+lab_seq+['O'])
                    for pred_chunk in pred_chunks:
                        if pred_chunk in label_chunks:
                            TP += 1
                        else:
                            FP += 1
                    for label_chunk in label_chunks:
                        if label_chunk not in pred_chunks:
                            FN += 1
    
                    input_line = words[idx]
                    word_tag_line = [input_line[_idx]+':'+lab_seq[_idx]+':'+pred_seq[_idx] for _idx in range(len(input_line))]
                    
                    if self.param.task_sc:
                        if self.param.multiClass:
                            pred_classes = [self.idx_to_class[i] for i,p in enumerate(snt_probs[idx]) if p > 0.5]
                            gold_classes = [self.idx_to_class[i] for i in raw_classes[idx]]
                            for pred_class in pred_classes:
                                if pred_class in gold_classes:
                                    TP2 += 1
                                else:
                                    FP2 += 1
                            for gold_class in gold_classes:
                                if gold_class not in pred_classes:
                                    FN2 += 1
                            gold_class_str = ';'.join(gold_classes)
                            pred_class_str = ';'.join(pred_classes)
                        else:
                            pred_class = self.idx_to_class[snt_probs[idx]]
                            if type(raw_classes[idx]) == int:
                                gold_classes = {self.idx_to_class[raw_classes[idx]]}
                            else:
                                gold_classes = set(raw_classes[idx])
                            if pred_class in gold_classes:
                                TP2 += 1
                            else:
                                FP2 += 1
                                FN2 += 1
                            gold_class_str = ';'.join(list(gold_classes))
                            pred_class_str = pred_class
                    else:
                        gold_class_str = ''
                        pred_class_str = ''
    
                    f.write(' '.join(word_tag_line)+' <=> '+gold_class_str+' <=> '+pred_class_str+'\n')
    
        if TP == 0:
            p, r, f = 0, 0, 0
        else:
            p, r, f = 100*TP/(TP+FP), 100*TP/(TP+FN), 100*2*TP/(2*TP+FN+FP)
        
        mean_losses = np.mean(losses, axis=0)
        return mean_losses, p, r, f, 0 if 2*TP2+FN2+FP2 == 0 else 100*2*TP2/(2*TP2+FN2+FP2)
        

    def train(self):
        print("Training starts at %s" % (time.asctime(time.localtime(time.time()))))
        best_f1, best_result = -1, {}

        train_data_index = np.arange(len(self.trainData.feats['data']))

        for i in range(self.param.max_epoch):
            start_time = time.time()
            losses = []
            # training data shuffle
            np.random.shuffle(train_data_index)
            self.model_tag.train()
            if self.param.fix_bert_model:
                self.model_tag.pretrained_model.eval()
            if self.param.task_sc:
                self.model_class.train()

            nsentences = len(train_data_index)
            piece_sentences = self.param.batchSize if int(nsentences * 0.1 / self.param.batchSize) == 0 else int(nsentences * 0.1 / self.param.batchSize) * self.param.batchSize
            for j in range(0, nsentences, self.param.batchSize):
                words, tags, raw_tags, classes, raw_classes, lens = data_reader.get_minibatch_with_class(self.trainData.feats['data'], self.trainData.tags['data'], self.trainData.intent['data'], self.tag_to_idx, self.class_to_idx, train_data_index, j, self.param.batchSize, 
                                                                                                        add_start_end=False, 
                                                                                                        multiClass=self.param.multiClass, 
                                                                                                        enc_dec_focus=self.param.enc_dec, 
                                                                                                        device=self.device)
                
                inputs = prepare_inputs_for_bert_xlnet(words, lens, self.tokenizer, 
                            cls_token_at_end=bool(self.param.pretrained_model_type in ['xlnet']),  # xlnet has a cls token at the end
                            cls_token=self.tokenizer.cls_token,
                            sep_token=self.tokenizer.sep_token,
                            cls_token_segment_id=2 if self.param.pretrained_model_type in ['xlnet'] else 0,
                            pad_on_left=bool(self.param.pretrained_model_type in ['xlnet']), # pad on the left for xlnet
                            pad_token_segment_id=4 if self.param.pretrained_model_type in ['xlnet'] else 0,
                            device=self.device)
                
                self.optimizer.zero_grad()
                if self.param.enc_dec:
                    tag_scores, encoder_info = self.model_tag(inputs, tags[:, :-1], lens, with_snt_classifier=True)
                    tag_loss = self.tag_loss_function(tag_scores.contiguous().view(-1, len(self.tag_to_idx)), tags[:, 1:].contiguous().view(-1))
                elif self.param.crf:
                    max_len = max(lens)
                    masks = [([1] * l) + ([0] * (max_len - l)) for l in lens]
                    masks = torch.tensor(masks, dtype=torch.uint8, device=device)
                    crf_feats, encoder_info = self.model_tag._get_lstm_features(inputs, lens, with_snt_classifier=True)
                    tag_loss = self.model_tag.neg_log_likelihood(crf_feats, masks, tags)
                else:
                    tag_scores, encoder_info = self.model_tag(inputs, lens, with_snt_classifier=True)
                    tag_loss = self.tag_loss_function(tag_scores.contiguous().view(-1, len(self.tag_to_idx)), tags.view(-1))
                if self.param.task_sc:
                    class_scores = self.model_class(self.encoder_info_filter(encoder_info))
                    class_loss = self.class_loss_function(class_scores, classes)
                    losses.append([tag_loss.item()/sum(lens), class_loss.item()/len(lens)])
                    total_loss = self.param.st_weight * tag_loss + (1 - self.param.st_weight) * class_loss
                else:
                    losses.append([tag_loss.item()/sum(lens), 0])
                    total_loss = tag_loss
                total_loss.backward()

                # Clips gradient norm of an iterable of parameters.
                if self.param.optimizer_sel.lower() != 'bertadam' and max_norm > 0:
                    torch.nn.utils.clip_grad_norm_(params, max_norm)

                if self.param.optimizer_sel.lower() == 'adamw':
                    self.scheduler.step()
                self.optimizer.step()

                if j % piece_sentences == 0:
                    print('[learning] epoch %i >> %2.2f%%'%(i,(j+self.param.batchSize)*100./nsentences),'completed in %.2f (sec) <<\r'%(time.time()-start_time), end='')
                    sys.stdout.flush()
            print('')

            mean_loss = np.mean(losses, axis=0)
            print('Training:\tEpoch : %d\tTime : %.4fs\tLoss of tag : %.2f\tLoss of class : %.2f ' % (i, time.time() - start_time, mean_loss[0], mean_loss[1]))
            gc.collect()

            self.model_tag.eval()
            if self.param.task_sc:
                self.model_class.eval()
            # Evaluation
            start_time = time.time()
            loss_val, p_val, r_val, f_val, cf_val = self.decode(self.validData.feats['data'], self.validData.tags['data'], self.validData.intent['data'], os.path.join(self.param.out_path, 'valid.iter'+str(i)))
            print('Validation:\tEpoch : %d\tTime : %.4fs\tLoss : (%.2f, %.2f)\tFscore : %.2f\tcls-F1 : %.2f ' % (i, time.time() - start_time, loss_val[0], loss_val[1], f_val, cf_val))

            if self.param.task_sc:
                val_f1_score = (self.param.st_weight * f_val + (1 - self.param.st_weight) * cf_val)
            else:
                val_f1_score = f_val
            if best_f1 < val_f1_score:
                self.model_tag.save_model(os.path.join(self.param.out_path, self.param.save_model_file_name+'.tag'))
                if self.param.task_sc:
                    self.model_class.save_model(os.path.join(self.param.out_path, self.param.save_model_file_name+'.class'))
                best_f1 = val_f1_score
                print('NEW BEST:\tEpoch : %d\tbest valid F1 : %.2f, cls-F1 : %.2f;' % (i, f_val, cf_val))
                best_result['iter'] = i
                best_result['vf1'], best_result['vcf1'], best_result['vce'] = f_val, cf_val, loss_val
        print('BEST RESULT: \tEpoch : %d\tbest valid (Loss: (%.2f, %.2f) F1 : %.2f cls-F1 : %.2f)' % (best_result['iter'], best_result['vce'][0], best_result['vce'][1], best_result['vf1'], best_result['vcf1']))
