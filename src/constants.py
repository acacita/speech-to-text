import os
from typing import List, NamedTuple, Union
from os.path import dirname, abspath
CONFIDENT_ENOUGH = 0.7


class SpeechContext:  # todo rethink about full version usage, if any ideas occur implement this type
    pass


RecognitionAudioShort = NamedTuple('NamedTuple', [('content', str)])
RecognitionAudioLong = NamedTuple('NamedTuple', [('uri', str)])
RecognitionAudio = Union[RecognitionAudioShort, RecognitionAudioLong]

RecognitionConfigFull = NamedTuple('RecognitionConfig', [('encoding', str),
                                                         ('sampleRateHertz', int),
                                                         ('audioChannelCount', int),
                                                         ('enableSeparateRecognitionPerChannel', bool),
                                                         ('languageCode', str),
                                                         ('maxAlternatives', int),
                                                         ('profanityFilter', bool),
                                                         ('speechContexts', List[SpeechContext]),
                                                         ('enableWordTimeOffsets', bool),
                                                         ('model', str),
                                                         ('useEnhanced', bool)])

RecognitionConfigShort = NamedTuple('RecognitionConfigShort', [("encoding", str),
                                                               ('languageCode', str),
                                                               ]
                                    )

RecognitionConfig = Union[RecognitionConfigFull, RecognitionConfigShort]

RecognizeRequest = NamedTuple('RecognizeRequest', [('config', RecognitionConfig),
                                                   ('audio', RecognitionAudio),
                                                   ])

def get_key():
    cwd = os.getcwd()
    rel_path = os.path.join(cwd, 'api-key.txt')
    with open(rel_path, 'r') as f:
        return f.read()

def recursive_to_json(obj : NamedTuple):
    _json = {}
    if isinstance(obj, tuple):
        datas = obj._asdict()
        for data in datas:
            if isinstance(datas[data], tuple):
                _json[data] = (recursive_to_json(datas[data]))
            else:
                _json[data] = (datas[data])
    return _json

API_KEY = get_key()
parent_dir = dirname(dirname(abspath('settings.py')))
UPLOADS_DIR = os.path.join(parent_dir, 'uploads')
CONFIDENT_ENOUGH = 0.7
