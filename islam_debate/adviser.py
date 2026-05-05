import logging
from typing import List

logger = logging.getLogger(__name__)


class Adviser:
    def __init__(
        self,
        llm_client,
        model: str,
        topic: str,
        position: str,
    ) -> None:
        self.llm_client = llm_client
        self.model: str = model
        self.topic: str = topic
        self.position: str = position
        self.responses: List[str] = []
        self.conversation_history: List[str] = []
        logger.info(f"{position} adviser initialized")

    def start(self) -> str:
        logger.info(f"Starting conversation as {self.position} position")
        initial_prompt: str = (
            f"You are partaking in a conversation about '{self.topic}'."
            f"You are to act as a {self.position}."
            f"Provide what you think is the most appropriate response given the chat history"
            f" and your position as a {self.position}."
        )
        response: str = self.llm_client.get_response(initial_prompt, self.model)
        self.responses.append(response)
        self.conversation_history.append(
            f"{self.position.capitalize()} opening statement: {response}"
        )
        logger.info(f"Opening statement generated for {self.position} position")
        return response

    def respond_to(self, client_statement: str) -> str:
        logger.info(f"Generating response for {self.position} position")
        self.conversation_history.append(f"{self.position.capitalize()}'s statement: {client_statement}")

        prompt: str = (
            f"You are participating in a conversation on the topic: '{self.topic}'. "
            f"You are to take a position of a {self.position}. Here's the conversation history "
            "so far:\n\n"
        )
        prompt += "\n\n".join(self.conversation_history)
        prompt += (
            f"\n\nProvide what you think is the most appropriate response given the chat history"
            f" and your position as a {self.position}." 
        )

        response: str = self.llm_client.get_response(prompt, self.model)
        self.responses.append(response)
        self.conversation_history.append(f"{self.position.capitalize()} response: {response}")
        logger.info(f"Response generated for {self.position} position")

        return response

    def conclude(self) -> str:
        logger.info(f"Generating conclusion for {self.position} position")
        prompt: str = (
            f"You have been participating in a conversation on the topic: '{self.topic}'. "
            f"You are taking the position of a {self.position}. Here's the entire conversation "
            "history:\n\n"
        )
        prompt += "\n\n".join(self.conversation_history)
        prompt += (
            "\n\nNow, provide a concluding statement for the conversation, summarizing your "
            "position and the key points you've made."
        )
        response: str = self.llm_client.get_response(prompt, self.model)
        self.responses.append(response)
        self.conversation_history.append(
            f"{self.position.capitalize()} conclusion: {response}"
        )
        logger.info(f"Conclusion generated for {self.position} position")

        return response
