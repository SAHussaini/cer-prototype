import json
import os
from inspect_ai import eval
from data.generate_data import *
from inspect_ai.model import GenerateConfig, get_model, Model
import pathlib
from inspect.task import belief_bias_task

config_json = {}
risks_json = {}

BASE_DIR = pathlib.Path(__file__).parent.resolve()

with open(
     os.path.join(BASE_DIR, "config.json"), 'r') as f:
        config_json = json.load(f)

DATA_DIR = config_json["data_dir"]

with open(os.path.join(DATA_DIR, "risks.json"), 'r') as f:
    risks_json = json.load(f)

user_model = get_model(
    config_json["user_model"]["name"],
    config=GenerateConfig(**config_json["user_model"]["config"])
)

assistant_model = get_model(
    config_json["assistant_model"]["name"],
    config=GenerateConfig(**config_json["assistant_model"]["config"])
)

monitoring_model_1 = get_model(
    config_json["monitoring_model_1"]["name"],
    config=GenerateConfig(**config_json["monitoring_model_1"]["config"])
)

monitoring_model_2 = get_model(
    config_json["monitoring_model_2"]["name"],
    config=GenerateConfig(**config_json["monitoring_model_2"]["config"])
)

def initialise_data(generator: DataGenerator):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    data = generator.generate_data()
    generator.save_data(data)

if config_json["tasks_to_run"]["belief_bias"]:
    initialise_data(BeliefBias())
    eval(
         belief_bias_task, 
         model_roles={
                "user": user_model,
                "assistant": assistant_model,
                "monitor_1": monitoring_model_1,
                "monitor_2": monitoring_model_2
         }
    )
    