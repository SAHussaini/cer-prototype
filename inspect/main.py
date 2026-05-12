import os

from data.generate_data import *
from config import *
from solver.dialogue_solver import dialogue_solver
from inspect_ai import Task, task
from inspect_ai.dataset import csv_dataset, FieldSpec
from inspect_ai.scorer import model_graded_fact
from inspect_ai.solver import generate, system_message
import json

if __name__ == "__main__":
    with open(DATA_DIR/"risks.json", 'r') as f:
        risks_json = json.load(f)

@task
def belief_bias_task() -> Task:
    # Generate data for belief bias
    belief_bias_generator = BeliefBias()
    belief_bias_data = belief_bias_generator.generate_data()
    belief_bias_generator.save_data(belief_bias_data)
    belief_bias_dataset = csv_dataset(os.path.join(DATA_DIR, "belief_bias.csv"))

    # Generate dialogue
    return Task(
        dataset=belief_bias_dataset,
        solver=dialogue_solver(
            # TODO: add arguments for models from config
            risk_type = risks_json["belief_bias"]["name"],
            risk_definition = risks_json["belief_bias"]["definition"],
        ),
        #TODO: make scorer to evaluate risk severity and probability for only flagged conversations
    )


