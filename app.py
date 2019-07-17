#!/usr/bin/env python

from flask import Flask
from flask import request
from deepspeech_model import deepspeech_model
from s3_download import get_file

model_dir = '/home/ec2-user/deepspeech/models/deepspeech-0.5.1-models/'
# model_dir = '/Users/raj.shah/projects/deepspeech/models2/deepspeech-0.5.1-models/'

smodel = model_dir + 'output_graph.pbmm'
strie = model_dir + 'trie'
salphabet = model_dir + 'alphabet.txt'
slm = model_dir + 'lm.binary'
file_dir = '/home/ec2-user/audiofiles/'

# file_dir  = './'

model = deepspeech_model(model=smodel,lm=slm,alphabet=salphabet,trie=strie)

app = Flask(__name__)

@app.route('/index', methods=['GET'])
def index():
    return 'Hi Josh'

@app.route('/indextwo', methods=['GET','POST'])
def indextwo():
    inp = request.args.get('filename',default=None,type=str)
    if(inp):
        print(inp)
    return 'Hi Josh'

@app.route('/get_text', methods=['POST'])
def get_text():
    inp = request.args.get('filename',default=None,type=str)
    if(inp):
        filepath = get_file(inp,file_dir)
    return model.infer(filepath)

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=80)
