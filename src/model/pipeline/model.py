import whisper_timestamped as whisper
import pickle as pk
from config.config import settings
def load_model(model_type=settings.model_type, device=settings.device):
    if settings.model_name == 'vosk-model-ru-0.22':
        pass
    else:
        model = whisper.load_model(model_type, device=device)
        pk.dump(model, open(f'{settings.model_path}/{settings.model_name}', 'wb'))

if settings.model_name == 'vosk-model-ru-0.22':
    pass
else:
    load_model()