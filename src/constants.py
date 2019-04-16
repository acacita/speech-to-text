import os
from typing import NamedTuple, Union
from os.path import dirname, abspath

CONFIDENT_ENOUGH = 0.7

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
                                                         ('enableWordTimeOffsets', bool),
                                                         ('model', str),
                                                         ('useEnhanced', bool)])

RecognitionConfigShort = NamedTuple('RecognitionConfigShort', [("encoding", str),
                                                               ('languageCode', str),
                                                               ('profanityFilter', bool)

                                                               ]
                                    )

RecognitionConfig = Union[RecognitionConfigFull, RecognitionConfigShort]

RecognizeRequest = NamedTuple('RecognizeRequest', [('config', RecognitionConfig),
                                                   ('audio', RecognitionAudio),
                                                   ])

SpeechRecognitionService = NamedTuple('SpeechRecognitionService', [('name', str),
                                                                   ('url', str),
                                                                   ('api_key', str)
                                                                   ])


def get_key(filename : str):
    cwd = os.getcwd()
    rel_path = os.path.join(cwd, filename)
    with open(rel_path, 'r') as f:
        return f.read()


def recursive_to_json(obj: NamedTuple):
    _json = {}
    if isinstance(obj, tuple):
        datas = obj._asdict()
        for data in datas:
            if isinstance(datas[data], tuple):
                _json[data] = (recursive_to_json(datas[data]))
            else:
                _json[data] = (datas[data])
    return _json


API_KEY = get_key('api-key.txt')
parent_dir = dirname(dirname(abspath('settings.py')))
UPLOADS_DIR = os.path.join(parent_dir, 'uploads')
CONFIDENT_ENOUGH = 0.7
