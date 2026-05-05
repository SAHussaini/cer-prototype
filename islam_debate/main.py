import argparse
import logging
import os
import time
from datetime import datetime
from typing import Any, Dict, List

from islam_debate.debater import Debater
from islam_debate.llm_clients import get_llm_client
from islam_debate.utils import generate_filename, save_html, save_json
from islam_debate.adviser import Adviser

logger = logging.getLogger(__name__)

LLM_CHOICES: List[str] = ["openai", "anthropic", "ollama"]
LOG_LEVELS: Dict[str, int] = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def main(model: str, topic: str, llm_type: str, num_rounds: int, mode: str="advise") -> Dict[str, Any]:
    if mode == 'advise':
        return advise(model, topic, llm_type, num_rounds)
    elif mode == 'debate':
        return debate(model, topic, llm_type, num_rounds)
    else:
        return {"error": f"Invalid mode: {mode}. Please choose 'advise' or 'debate'."}
    
def advise(model: str, topic: str, llm_type: str, num_rounds: int) -> Dict[str, Any]:
    start_time = time.time()
    llm_client = get_llm_client(llm_type)
    client: Adviser = Adviser(llm_client, model, topic, "teenager having radical ideation")
    adviser: Adviser = Adviser(llm_client, model, topic, "agent the teenager trusts")

    conversation_results: Dict[str, Any] = {
        "metadata": {
            "model": model,
            "topic": topic,
            "llm_type": llm_type,
            "num_rounds": num_rounds,
            "date": datetime.now().isoformat(),
        },
        "conversation": {},
    }

    logger.info("Starting conversation...")
    conversation_results["conversation"]["opening_arguments"] = {
        "client": client.start(),
        "adviser": adviser.start(),
    }

    logger.debug("\nInitial arguments:")
    logger.debug(f"Client: {conversation_results['conversation']['opening_arguments']['client']}")
    logger.debug(
        f"\nAdviser: {conversation_results['conversation']['opening_arguments']['adviser']}"
    )

    for round in range(1, num_rounds + 1):
        logger.debug(f"\nRound {round}:")
        round_key = f"round_{round}"
        conversation_results["conversation"][round_key] = {
            "client": client.respond_to(adviser.responses[-1]),
            "adviser": adviser.respond_to(client.responses[-1]),
        }

        logger.debug(f"Client: {conversation_results['conversation'][round_key]['client']}")
        logger.debug(f"\nAdviser: {conversation_results['conversation'][round_key]['adviser']}")

    logger.debug("\nConcluding statements:")
    conversation_results["conversation"]["conclusions"] = {
        "client": client.conclude(),
        "adviser": adviser.conclude(),
    }

    logger.debug(f"Client: {conversation_results['conversation']['conclusions']['client']}")
    logger.debug(f"\nAdviser: {conversation_results['conversation']['conclusions']['adviser']}")

    end_time = time.time()
    conversation_results["metadata"]["time_taken"] = end_time - start_time

    return conversation_results

def debate(model: str, topic: str, llm_type: str, num_rounds: int) -> Dict[str, Any]:
    start_time = time.time()
    llm_client = get_llm_client(llm_type)
    for_debater: Debater = Debater(llm_client, model, topic, "for")
    against_debater: Debater = Debater(llm_client, model, topic, "against")

    debate_results: Dict[str, Any] = {
        "metadata": {
            "model": model,
            "topic": topic,
            "llm_type": llm_type,
            "num_rounds": num_rounds,
            "date": datetime.now().isoformat(),
        },
        "debate": {},
    }

    logger.info("Starting debate...")
    debate_results["debate"]["opening_arguments"] = {
        "for": for_debater.start(),
        "against": against_debater.start(),
    }

    logger.debug("\nInitial arguments:")
    logger.debug(f"For: {debate_results['debate']['opening_arguments']['for']}")
    logger.debug(
        f"\nAgainst: {debate_results['debate']['opening_arguments']['against']}"
    )

    for round in range(1, num_rounds + 1):
        logger.debug(f"\nRound {round}:")
        round_key = f"round_{round}"
        debate_results["debate"][round_key] = {
            "for": for_debater.respond_to(against_debater.responses[-1]),
            "against": against_debater.respond_to(for_debater.responses[-1]),
        }

        logger.debug(f"For: {debate_results['debate'][round_key]['for']}")
        logger.debug(f"\nAgainst: {debate_results['debate'][round_key]['against']}")

    logger.debug("\nConcluding statements:")
    debate_results["debate"]["conclusions"] = {
        "for": for_debater.conclude(),
        "against": against_debater.conclude(),
    }

    logger.debug(f"For: {debate_results['debate']['conclusions']['for']}")
    logger.debug(f"\nAgainst: {debate_results['debate']['conclusions']['against']}")

    end_time = time.time()
    debate_results["metadata"]["time_taken"] = end_time - start_time

    return debate_results


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Run a debate between two LLMs."
    )
    parser.add_argument("llm_type", choices=LLM_CHOICES, help="Type of LLM to use")
    parser.add_argument("model", help="Model name for the chosen LLM")
    parser.add_argument("topic", help="Topic of the debate")
    parser.add_argument(
        "--rounds", type=int, default=3, help="Number of debate rounds (default: 3)"
    )
    parser.add_argument(
        "--log-level",
        choices=LOG_LEVELS.keys(),
        default="INFO",
        help="Set the logging level",
    )
    parser.add_argument(
        "--filename", help="Custom output filename (without extension)", default=None
    )
    parser.add_argument(
        "--return_html",
        help="Return a html file that makes it easier to read responses",
        default=False,
    )
    args: argparse.Namespace = parser.parse_args()

    logging.basicConfig(
        level=LOG_LEVELS[args.log_level],
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    script_path = os.path.abspath(__file__)
    logger.info(f"Running script: {script_path}")

    results = main(args.model, args.topic, args.llm_type, args.rounds)

    if not args.filename:
        filename = generate_filename(args.topic)

    json_path = save_json(results, filename)
    logger.info(f"Debate results saved to JSON: {json_path}")

    if args.return_html:
        html_path = save_html(results, filename)
        logger.info(f"Debate results saved to HTML: {html_path}")
