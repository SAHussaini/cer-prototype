from data.generate_data import *
from config import *
from inspect_ai import Task, task
from inspect_ai.dataset import example_dataset
from inspect_ai.scorer import model_graded_fact
from inspect_ai.solver import generate, system_message

if __name__ == "__main__":
    # Generate data for belief bias
    belief_bias_generator = BeliefBias()
    belief_bias_data = belief_bias_generator.generate_data()
    belief_bias_generator.save_data(belief_bias_data)

    # Generate dialogue
    


