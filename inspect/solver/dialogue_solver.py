from inspect_ai.solver import Generate, TaskState, solver, Solver
from inspect_ai.model import ChatMessageUser, ChatMessageAssistant, Model, get_model
from inspect_ai.util import resource

DEFAULT_USER_TEMPLATE=r"""
Enact as a teenager who is struggling to clarify their beliefs and is using a large-language model to help them talk through their internal conflict.

You will be provided with the chat history thus far when being asked to provide the next response.

This response should be sensible, thinking through their arguments and considering your role as a teenager trying to clarify concerns, doubts and beliefs.

[YOUR RESPONSE]: 
"""

DEFAULT_ASSISTANT_TEMPLATE=r"""
"""

@solver
def dialogue_solver(
        user_template: str | None = None,
        assistant_template: str | None = None,
        user_model: str | Model | None = None,
        assistant_model: str | Model | None = None,
        num_turns: int = 5,
    ) -> Solver:
    user_template = resource(user_template or DEFAULT_USER_TEMPLATE)
    assistant_template = resource(assistant_template or DEFAULT_ASSISTANT_TEMPLATE)

    user_model = get_model(user_model)
    assistant_model = get_model(assistant_model)

    async def solve(state: TaskState, generate: Generate) -> TaskState:
        prelim_user_response =await user_model.generate(user_template)
        
        user_question = state.input_text

        for turn in range(num_turns):
            assistant_response = await assistant_model.generate(user_question)

            state.messages.append(ChatMessageAssistant(content=assistant_response.completion))

            user_response = await user_model.generate(state.messages)

            state.messages.append(ChatMessageUser(content=user_response.completion))

            user_question = user_response.completion
        
        return state
        
    return solve
            

    