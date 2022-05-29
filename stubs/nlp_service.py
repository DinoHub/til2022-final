from typing import Iterable, List
from tilsdk.localization.types import *
from io import BytesIO

import soundfile as sf
import tensorflow as tf
import librosa
import onnxruntime as ort

class NLPService:
    def __init__(self, model_dir:str):
        '''
        Parameters
        ----------
        model_dir : str
            Path of model file to load.
        '''
        self.session = ort.InferenceSession(model_dir, providers=["CUDAExecutionProvider"])

    def locations_from_clues(self, clues:Iterable[Clue]) -> List[RealLocation]:
        '''Process clues and get locations of interest.
        
        Parameters
        ----------
        clues
            Clues to process.

        Returns
        -------
        lois
            Locations of interest.
        '''

        locations = []
        for c in clues:
            waveform, sr = sf.read(BytesIO(c.audio))

            # feature extraction
            mel_spec = librosa.feature.melspectrogram(y=waveform, sr=sr).T
            mfcc = librosa.feature.mfcc(y=waveform, sr=sr).T
            chr = librosa.feature.chroma_stft(y=waveform, sr=sr).T
            sc = librosa.feature.spectral_contrast(S=np.abs(librosa.stft(waveform)), sr=sr).T
            features = np.hstack([mel_spec, mfcc, chr, sc])
            
            padded = tf.keras.preprocessing.sequence.pad_sequences([features], maxlen=216, dtype=np.float32, padding='post')
            padded = np.expand_dims(padded, axis=3)

            probabilities = self.session.run(["dense"], {"Inp": padded})
            prediction = np.argmax(probabilities)
            
            if prediction == 0:     # location of interest
                locations.append(c.location)

        return locations

class MockNLPService:
    '''Mock NLP Service.
    
    This is provided for testing purposes and should be replaced by your actual service implementation.
    '''

    def __init__(self, model_dir:str):
        '''
        Parameters
        ----------
        model_dir : str
            Path of model file to load.
        '''
        pass

    def locations_from_clues(self, clues:Iterable[Clue]) -> List[RealLocation]:
        '''Process clues and get locations of interest.
        
        Mock returns location of all clues.
        '''
        locations = [c.location for c in clues]

        return locations