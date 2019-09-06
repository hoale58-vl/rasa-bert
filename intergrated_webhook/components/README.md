# Install module langdetect
pip install langdetect -> Not need
pip install langid

# Install CocCoc tokenizer
git clone https://github.com/coccoc/coccoc-tokenizer
sudo apt-get install gcc cmake
pip install Cython
cmake -DBUILD_PYTHON=1 ..
sudo make install
cp -r /usr/local/lib/python3.6/site-packages/CocCocTokenizer* /home/black/anaconda3/envs/rasa/lib/python3.6/site-packages/

cd python
python setup.py install

# Install Pyvi
pip install pyvi

# Install bert nlu
pip install pytorch-pretrained-bert
pip install gpustat

# Clone bert slot_tagger respository 
git clone https://github.com/sz128/slot_filling_and_intent_detection_of_SLU/
mv slot_filling_and_intent_detection_of_SLU/* bert_nlu/lib/
