from __future__ import absolute_import, division, print_function

import argparse
import numpy as np
import shlex
import subprocess
import sys
import wave

from deepspeech import Model, printVersions
from timeit import default_timer as timer

try:
    from shhlex import quote
except ImportError:
    from pipes import quote

# Define the sample rate for audio

SAMPLE_RATE = 16000
# These constants control the beam search decoder

# Beam width used in the CTC decoder when building candidate transcriptions
BEAM_WIDTH = 500

# The alpha hyperparameter of the CTC decoder. Language Model weight
LM_ALPHA = 0.75

# The beta hyperparameter of the CTC decoder. Word insertion bonus.
LM_BETA = 1.85


# These constants are tied to the shape of the graph used (changing them changes
# the geometry of the first layer), so make sure you use the same constants that
# were used during training

# Number of MFCC features to use
N_FEATURES = 26

# Size of the context window used for producing timesteps in the input vector
N_CONTEXT = 9


class deepspeech_model:
    def __init__(self, model,alphabet,lm=None,trie=None):

        self.model = Model(model, N_FEATURES, N_CONTEXT,alphabet, BEAM_WIDTH)
        if(lm and trie):
            self.model.enableDecoderWithLM(alphabet,lm, trie, LM_ALPHA, LM_BETA)

    def infer(self,audiofile):
        fin = wave.open(audiofile, 'rb')
        fs = fin.getframerate()
        if fs != SAMPLE_RATE:
            print('Warning: original sample rate ({}) is different than {}hz. Resampling might produce erratic speech recognition.'.format(fs, SAMPLE_RATE), file=sys.stderr)
            fs, audio = self.convert_samplerate(audiofile)
        else:
            audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)

        audio_length = fin.getnframes() * (1/SAMPLE_RATE)
        fin.close()

        return self.model.stt(audio, fs)

    def convert_samplerate(self,audio_path):
        sox_cmd = '/usr/local/bin/sox {} --type raw --bits 16 --channels 1 --rate {} --encoding signed-integer --endian little --compression 0.0 --no-dither - '.format(quote(audio_path), SAMPLE_RATE)
        try:
            output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            raise RuntimeError('SoX returned non-zero status: {}'.format(e.stderr))
        except OSError as e:
            raise OSError(e.errno, 'SoX not found, use {}hz files or install it: {}'.format(SAMPLE_RATE, e.strerror))

        return SAMPLE_RATE, np.frombuffer(output, np.int16)
