from cnnClassifier.config.configuration import ConfigurationManager
from cnnClassifier.components import prepare_callbacks, training
from cnnClassifier import logger
from pathlib import Path

STAGE_NAME = "Training"

class ModelTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()

        
        prepare_callbacks_config = config.get_prepare_callbacks_config()
        prepare_cb = prepare_callbacks.PrepareCallbacks(config=prepare_callbacks_config)
        callback_list = prepare_cb.get_tb_ckpt_callbacks()

        training_config = config.get_training_config()
        trainer = training.Training(config=training_config)
        trainer.get_base_model()
        trainer.train_valid_generator()
        trainer.train(callbacks_list=callback_list)

if __name__ == '__main__':
    try:
        logger.info(f"*******************")
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = ModelTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
