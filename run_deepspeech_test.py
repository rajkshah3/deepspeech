from deepspeech_model import deepspeech_model
wd = '/Users/raj.shah/projects/deepspeech/models/'
model = deepspeech_model(model=wd+'output_graph.pbmm',alphabet=wd+'alphabet.txt',lm=wd+'lm.binary',trie=wd+'trie')

# import pdb; pdb.set_trace()  # breakpoint 6da0f341 //

audiofile=wd+'audio/2830-3980-0043.wav'
text = model.infer(audiofile)

print(text)
import pdb; pdb.set_trace()  # breakpoint 6da0f341 //

print('dome')