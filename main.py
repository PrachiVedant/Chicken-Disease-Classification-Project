from cnnClassifier import logger
from cnnClassifier.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from cnnClassifier.pipeline.stage_02_prepare_base_model import PrepareBaseModelPipeline
from cnnClassifier.pipeline.stage_03_training import ModelTrainingPipeline
from cnnClassifier.pipeline.stage_04_evaluation import EvaluationPipeline
from pathlib import Path

STAGE_NAME= "Data Ingestion stage"
try:
    logger.info(f">>>>>>Stage Name {STAGE_NAME} started !!! <<<<<<")
    data_ingestion= DataIngestionPipeline()
    data_ingestion.main()
    logger.info(f">>>>>>Stage Name {STAGE_NAME} completed !!! <<<<<< \n\nx=======x")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME= "Prepare Base Model"
try:
    logger.info(f">>>>>>Stage Name {STAGE_NAME} started !!! <<<<<<")
    prepare_base_model = PrepareBaseModelPipeline()
    prepare_base_model.main()
    logger.info(f">>>>>>Stage Name {STAGE_NAME} completed !!! <<<<<< \n\nx=======x")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME= "Training"
try:
    logger.info(f"*******************")
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    model_trainer =ModelTrainingPipeline()
    model_trainer.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Evaluation stage"
try:
   logger.info(f"*******************")
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
   model_evalution = EvaluationPipeline()
   model_evalution.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

except Exception as e:
        logger.exception(e)
        raise e
