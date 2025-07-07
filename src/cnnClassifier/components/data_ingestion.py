import os
import urllib.request as request
import zipfile
from cnnClassifier import logger
from cnnClassifier.utils.common import get_size
from cnnClassifier.entity.config_entity import (DataIngestionConfig)
from pathlib import Path

class DataIngestion:
    def __init__(self,config : DataIngestionConfig):
        self.config=config

    def download_path(self):
        if not os.path.exists(self.config.local_data_file):
            filename,headers=request.urlretrieve(
                url=self.config.source_URL,
                filename=self.config.local_data_file
            )
            logger.info(f"{filename} downloaded ! with the following path : \n{headers}")
        else:
            logger.info(f"File already exists of size : {get_size(Path(self.config.local_data_file))}")

    def extract_zip_file(self):
        unzip=self.config.unzip_dir
        os.makedirs(unzip, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file , 'r') as zipref:
            zipref.extractall(unzip)