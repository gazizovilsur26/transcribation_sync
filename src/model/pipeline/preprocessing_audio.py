import os
import librosa as lr
import soundfile as sf
import warnings
import logging
from typing import List
from config.config import settings
from loguru import logger
warnings.filterwarnings("ignore")

class AudioProcessor:
    def __init__(self, sample_rate=16000, channels=['left', 'right'], **kwargs):
        self.sample_rate = sample_rate
        self.channels = channels
        logging.basicConfig(**kwargs)

    @staticmethod
    def split_audio_to_segments(wav):
        try:
            audio_segments = [
                {
                    'channel': 'left',
                    'wav': wav[0],
                    'start': 0,
                    'end': len(wav[0])
                },
                {
                    'channel': 'right',
                    'wav': wav[1],
                    'start': 0,
                    'end': len(wav[1])
                }
            ]
            return audio_segments
        except Exception as e:
            logging.error(f'Error during audio segmentation: {e}')

    def split_audio(self, audio_path, output_path):
        try:
            wav, _ = lr.load(str(audio_path[1]), sr=self.sample_rate, mono=False)
            audio_segments = self.split_audio_to_segments(wav)

            for segment in audio_segments:
                start = segment['start']
                end = segment['end']
                channel = segment['channel']
                audio_id = audio_path[0]

                new_filename = f'{audio_id}_{start}_{end}_{channel}.wav'
                new_path = os.path.join(output_path, new_filename)

                sf.write(new_path, segment['wav'], samplerate=self.sample_rate)

        except Exception as e:
            logging.error(f'Error during audio splitting: {e}')

def split_audio_all(audio_processor):
    logger.info(f'spliting audio from {settings.audio_path} to left and right channel')
    for audio in os.listdir(settings.audio_path):
        audio_path = ['audio_id', f'{settings.audio_path}/{audio}']
        output_path = settings.output_path
        audio_processor.split_audio(audio_path, output_path)

# audio_processor = AudioProcessor()
# split_audio_all(audio_processor = audio_processor)