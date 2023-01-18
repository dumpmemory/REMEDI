"""Randomly initialize a model and save it."""
import argparse
import logging
from pathlib import Path

from src import models
from src.utils import env_utils, experiment_utils, logging_utils

logger = logging.getLogger(__name__)


def main(args: argparse.Namespace) -> None:
    """Randomly initialized the model and save it."""
    logging_utils.configure(args=args)

    mt = models.load_model(args.model, device="cpu", fp16=args.fp16)
    model = mt.model

    logger.info(f"reinitialization model with seed {args.seed}")
    experiment_utils.set_seed(args.seed)
    model.init_weights()

    out_file = args.out_file
    if out_file is None:
        out_file = env_utils.determine_models_dir() / f"{args.model}_random"

    logger.info(f"saving random model to {out_file}")
    model.save_pretrained(str(out_file))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="load a model and random init it")
    parser.add_argument("--out-file", type=Path, help="path to save model")
    parser.add_argument("--seed", type=int, default=123456, help="random seed")
    models.add_model_args(parser)
    logging_utils.add_logging_args(parser)
    args = parser.parse_args()
    main(args)
