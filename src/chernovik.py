from config.config import settings
from model.model_service import Transcribation
import os
from model.pipeline.preprocessing_audio import AudioProcessor, split_audio_all
from loguru import logger
import warnings
warnings.filterwarnings("ignore")
from multiprocessing import Pool
from vosk import Model, KaldiRecognizer, SetLogLevel
import wave
import json

def main():
    logger.info('running the application...')
    print('Начинаем')
    audio_processor = AudioProcessor()
    print('Разделение на каналы')
    split_audio_all(audio_processor = audio_processor)
    transcribation = Transcribation()
    print('Загрузка модели')
    transcribation.load_model()
    print('Транскрибация')
    transcribation.transcribe()
    print('Схлопывание')
    folder_path = settings.output_dir
    logger.info('start combining left channel text with right channel text')
    for filename in os.listdir(folder_path):
        if filename.endswith("_left.json"):
            left_filename = filename
            right_filename = filename.replace("_left.json", "_right.json")
            


            transcribation.combine_dialog(left_filename, right_filename)
    print('Конец')

if __name__ == '__main__':
    main()

# # @logger.catch
# def main():
#     logger.info('running the application...')
#     audio_processor = AudioProcessor()
#     split_audio_all(audio_processor = audio_processor)
#     print('1')

#     trans = Transcribation()
#     trans.load_model()
#     print('2')
    

#     # load_model = LoadModel()
#     # load_model.load_model()
#     # model = load_model.model
#     # ml_svc = ModelService(input_path=settings.output_path, model=model)
#     # ml_svc.load_model(model_name=settings.model_name)

#     # ml_svc.transcribe()
#     def pool_handler_4(output_dir = settings.output_dir): # Объект для параллельного транскрибирования
        
#         p = Pool(2) # ЗАДАЙ КОЛ-ВО ЯДЕР!!!!!!!!! 
#         p.map(trans.transcribate, [(wav_file, output_dir) for wav_file in os.listdir(trans.input_path)])

#     pool_handler_4() 
#     print('3')
#     # folder_path = settings.output_dir
#     # logger.info('start combining left channel text with right channel text')
#     # for filename in os.listdir(folder_path):
#     #     if filename.endswith("_left.json"):
#     #         left_filename = filename
#     #         right_filename = filename.replace("_left.json", "_right.json")
            


#     #         ml_svc.combine_dialog(left_filename, right_filename)

# if __name__ == '__main__':
#     main()
