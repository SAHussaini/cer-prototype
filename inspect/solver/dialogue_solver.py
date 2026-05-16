from inspect_ai.solver import Generate, TaskState, solver, Solver
from inspect_ai.model import ChatMessageUser, ChatMessageAssistant, Model, get_model
from inspect_ai.scorer import Target, score, model_graded_qa
from inspect_ai.util import resource
import random

# Model for storing risk evaluation
class RiskEvaluation:
    score: float
    explanation: str

    def __init__(self, score: float, explanation: str = ""):
        self.score = score
        self.explanation = explanation

@solver
def dialogue_solver(
        user_template: str = "",
        assistant_template: str = "",
        monitoring_template: str = "",
        monitoring_criteria: str = "",
        monitoring_probability: float = 0.25,
        num_turns: int = 5,
        risk_type: str = "",
        risk_definition: str = ""
    ) -> Solver:
    user_model = get_model(role="user")
    assistant_model = get_model(role="assistant")
    monitoring_models: list[str | Model] = [get_model(role="monitor_1"), get_model(role="monitor_2")]

    risk_scores: list[float] = []

    async def update_risk_scores(state: TaskState, system_prompt: str, criteria: str):
        score = await model_graded_qa(
            template = system_prompt,
            include_history = True,
            model = monitoring_models,
            partial_credit = True
        )(state, Target(criteria))

        if score:
            risk_scores.append(score.as_float())
        
        return score

    async def solve(state: TaskState, generate: Generate) -> TaskState:
        user_system_prompt = user_template.format(initial_question=state.input_text)
        assistant_system_prompt = assistant_template
        monitoring_system_prompt = monitoring_template.format(risk_type=risk_type, risk_definition=risk_definition)
        criteria = monitoring_criteria.format(risk_type=risk_type, risk_definition=risk_definition)

        user_model.config.system_message = user_system_prompt
        assistant_model.config.system_message = assistant_system_prompt

        state.messages.append(ChatMessageUser(content=state.input_text))

        for turn in range(num_turns):
            assistant_response = await assistant_model.generate(
                state.messages,
            )
            state.messages.append(ChatMessageAssistant(content=assistant_response.completion))

            if random.randint(0, 100) < (monitoring_probability * 100):
                await update_risk_scores(state, monitoring_system_prompt, criteria)

            user_response = await user_model.generate(
                state.messages,
            )
            state.messages.append(ChatMessageUser(content=user_response.completion))
        
        last_score = await update_risk_scores(state, monitoring_system_prompt, criteria)
        
        state.store.set(
            str(state.sample_id), 
            RiskEvaluation(
                score = sum(risk_scores) / len(risk_scores) if risk_scores else 0.0,
                explanation = str(last_score.explanation) if last_score else ""
            )
        )

        return state

    return solve
            

    