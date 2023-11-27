import json
import whisper_timestamped as whisper
import os
from pathlib import Path
from model.pipeline.model import load_model
import pickle as pk
from config.config import settings
from loguru import logger
from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import wave
import multiprocessing

class ModelService:
    def __init__(self, input_path):
        self.input_path = input_path
        self.model = None

    def load_model(self):
        logger.info('Model selection...')
        if settings.model_name == 'vosk-model-ru-0.22':
            logger.info(f'Selected model for transcription: {settings.model_name}')
            self.model = Model("model/models/vosk-model-ru-0.22")
            SetLogLevel(0)
        else:
            logger.info(f'Selected model for transcription: {settings.model_name}')
            logger.info(f'Checking the existence of model config file at {settings.model_path}/{settings.model_name}')
            model_path = Path(f'{settings.model_path}/{settings.model_name}')
            if not model_path.exists():
                logger.warning(f'Model at {settings.model_path}/{settings.model_name} was not found --> building {settings.model_name}')
                load_model()
            logger.info(f'Model {settings.model_name} exists! --> loading model configuration file')

    def transcribe_whisper(self, wav_file, output_dir):
        if wav_file.endswith('.wav'):
            wav_path = os.path.join(self.input_path, wav_file)
            audio = whisper.load(wav_path)
            result = whisper.transcribe(self.model, audio, language="ru")
            json_string = json.dump(result, ensure_ascii=False, indent=2)
            json_filename = os.path.splitext(wav_file)[0] + ".json"
            json_path = os.path.join(output_dir, json_filename)
            with open(json_path, mode="w", encoding="utf-8") as file:
                file.write(json_string)

    def transcribe_vosk(self, wav_file, output_dir):
        if wav_file.endswith(".wav"):
            wav_path = os.path.join(self.input_path, wav_file)

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            wf = wave.open(wav_path, "rb")
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
                print("Audio file must be WAV format mono PCM.")
                exit(1)

            rec = KaldiRecognizer(self.model, wf.getframerate())
            rec.SetWords(True)

            results = []

            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    results.append(result)

            final_result = json.loads(rec.FinalResult())
            results.append(final_result)

            transformed_data = {
                "segments": []
            }
            for i in range(len(results)):
                try:
                    new_dict = {
                        "text": results[i]['text'],
                        "start": results[i]['result'][0]['start'],
                        "end": results[i]['result'][-1]['end'],
                        "words": results[i]['result'][-1]['end']
                    }
                    transformed_data["segments"].append(new_dict)
                except:
                    pass

            json_string = json.dumps(transformed_data, indent=2, ensure_ascii=False)
            json_filename = os.path.splitext(wav_file)[0] + ".json"
            json_path = os.path.join(output_dir, json_filename)

            with open(json_path, 'w', encoding='utf-8') as file:
                file.write(json_string)

    def transcribe(self):
        self.load_model()
        output_dir = settings.output_dir
        if settings.model_name == 'whisper_timestamped_large':
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            pool = multiprocessing.Pool(processes=2)
            pool.starmap(self.transcribe_whisper, [(wav_file, output_dir) for wav_file in os.listdir(self.input_path)])
            pool.close()
            pool.join()

        if settings.model_name == 'vosk-model-ru-0.22':
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            pool = multiprocessing.Pool(processes=3)
            pool.starmap(self.transcribe_vosk, [(wav_file, output_dir) for wav_file in os.listdir(self.input_path)])
            pool.close()
            pool.join()
