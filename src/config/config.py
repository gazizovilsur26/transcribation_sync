from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import DirectoryPath
from loguru import logger

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='config/.env', env_file_encoding='utf-8')
    
    audio_path: DirectoryPath
    output_path: DirectoryPath
    model_type: str
    device: str
    model_path: DirectoryPath
    model_name: str
    output_dir: DirectoryPath
    combined_dialogs_path: DirectoryPath
    log_level: str



settings = Settings()
logger.remove()
logger.add('logs/app.log',rotation='1 day', retention='1 week', compression='zip', level=settings.log_level)

    

