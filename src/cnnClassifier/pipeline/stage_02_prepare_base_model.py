from cnnClassifier.config.configuration import ConfigurationManager
from cnnClassifier.components.prepare_base_model import PrepareBaseModel
from cnnClassifier import logger
from pathlib import Path

STAGE_NAME= "Prepare Base Model"

class PrepareBaseModelPipeline:
    def __init__(self):
        pass
    def main(self):
        try:
            config= ConfigurationManager()
            prepare_base_model_config = config.get_prepare_base_model_config()
            prepare_base_model = PrepareBaseModel(config=prepare_base_model_config)
            prepare_base_model.get_base_model()
            prepare_base_model.update_model()

        except Exception as e:
            raise e
        


if __name__ == "__main__":
    try:
        logger.info(f">>>>>>Stage Name {STAGE_NAME} started !!! <<<<<<")
        obj = PrepareBaseModelPipeline()
        obj.main()
        logger.info(f">>>>>>Stage Name {STAGE_NAME} completed !!! <<<<<< \n\nx=======x")
    except Exception as e:
        logger.exception(e)
        raise e