from cnnClassifier.config.configuration import ConfigurationManager
from cnnClassifier.components.data_ingestion import DataIngestion
from cnnClassifier import logger

STAGE_NAME= "Data Ingestion stage"

class DataIngestionPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config=ConfigurationManager()
            data_ingestion_config  = config.get_data_ingestion_config()
            data_ingestion=DataIngestion(config=data_ingestion_config)
            data_ingestion.download_path()
            data_ingestion.extract_zip_file()
        except Exception as e:
            raise e
        
if __name__ == "__main__":
    try:
        logger.info(f">>>>>>Stage Name {STAGE_NAME} started !!! <<<<<<")
        obj = DataIngestionPipeline()
        obj.main()
        logger.info(f">>>>>>Stage Name {STAGE_NAME} completed !!! <<<<<< \n\nx=======x")
    except Exception as e:
        logger.exception(e)
        raise e

