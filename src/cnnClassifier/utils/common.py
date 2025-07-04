import os
from box.exceptions import BoxValueError
import yaml
from cnnClassifier import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from box.exceptions import BoxValueError
from pathlib import Path
from typing import Any, Union, List
import base64

#@ensure_annotations
def read_yaml(path_to_yaml : Path) -> ConfigBox:
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            print("✅ DEBUG YAML PATH:", path_to_yaml)
            print("✅ DEBUG YAML CONTENT:", repr(content), type(content))

            if content is None or (isinstance(content, dict) and len(content) == 0):
                raise ValueError("yaml file is empty or invalid")

            try:
                config_box = ConfigBox(content)
                return config_box
            except BoxValueError as e:
                print(f"❌ BoxValueError details: {e}")
                print(f"❌ Problematic content: {repr(content)}")
                raise
    except Exception as e:
        print(f"❌ Exception: {e}")
        raise




# @ensure_annotations  
def create_directories(paths: Union[str, Path, List[Union[str, Path]]], verbose: bool = True):
    if isinstance(paths, (str, Path)):
        paths = [paths]

    for path in paths:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Created directory at: {path}")


#@ensure_annotations
def save_json(path: Path , data: dict):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
    logger.info(f"json file saved at : {path}")

#@ensure_annotations
def load_json(path:Path) -> ConfigBox :
    with open(path, 'r') as f:
        content=json.load(f)
    logger.info(f"json file loaded succesfully from: {path}")
    return ConfigBox(content)

#@ensure_annotations
def save_bin(data: any, path : Path):
    joblib.dump(value=data , filename=path)
    logger.info(f"Binary file saved at : {path}")

#@ensure_annotations
def load_bin(path: Path) ->Any:
    data=joblib.load(path)
    logger.info(f"Binary file loaded succesfully from: {path}")
    return data

#@ensure_annotations
def get_size(path: Path) -> str:
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"

def decodeImage(imgstring , filename):
    imgdata = base64.b64decode(imgstring)
    with open(filename , 'wb') as f:
        f.write(imgdata)
        f.close()

def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())