import os

from data.generate_data import *
from solver.dialogue_solver import dialogue_solver
from inspect_ai import Task, task
from inspect_ai.dataset import csv_dataset, FieldSpec
from inspect_ai.scorer import model_graded_fact
from inspect_ai.solver import generate, system_message
from main import DATA_DIR, user_model, assistant_model, monitoring_model_1, monitoring_model_2, risks_json

@task
def belief_bias_task() -> Task:
    belief_bias_dataset = csv_dataset(os.path.join(DATA_DIR, "belief_bias.csv"))

    return Task(
        dataset=belief_bias_dataset,
        solver=dialogue_solver(
            user_template=risks_json["belief_bias"]["user_template"],
            assistant_template=risks_json["belief_bias"]["assistant_template"],
            monitoring_template=risks_json["belief_bias"]["monitoring_template"],
            monitoring_criteria=risks_json["belief_bias"]["monitoring_criteria"],
            risk_type = risks_json["belief_bias"]["name"],
            risk_definition = risks_json["belief_bias"]["definition"],
        ),
        #TODO: make scorer to evaluate risk severity and probability for only flagged conversations
    )


