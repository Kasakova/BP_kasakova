#!/usr/bin/env python3
# coding: utf-8


import argparse
import logging
from t5s import *

class T52(T5):
    def load_model(self):
        if self.model is not None:
            return self.model

        # Load the pre-trained model
        model_config = self.config["t5_model"]
        if "load_checkpoint" in model_config:
            model_fn = model_config["load_checkpoint"]
        else:
            model_fn = model_config["pre_trained"]

        self.logger.info("Loading model from %s", model_fn)
        self.model = T5Training.from_pretrained(model_fn,from_pt=True)
        return self.model

logger = logging.getLogger('t5s.fine_tune')

parser = argparse.ArgumentParser(description='T5 fine-tuner')
parser.add_argument('config', metavar='YAML', type=str, help='Configuration YAML file')

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)-10s %(message)s', level=logging.DEBUG)

    args = parser.parse_args()

    t5 = T52(args.config)
    t5.fine_tune()