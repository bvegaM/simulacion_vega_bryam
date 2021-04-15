import argparse
import coloredlogs
import logging
logging.basicConfig(level=logging.INFO)
import pandas as pd
import numpy as np

from models import Model
from utils import Utils
from transform import Transform



logger = logging.getLogger(__name__)
coloredlogs.install()

def main(filename):
    logger.info("================ Starting machine learning model process ================")

    try:
        utils = Utils()
        models = Model()

        df = utils._read_from_csv(filename)
        transform = Transform(df,5,2)
        features,target = transform._transform_process()
        x_train,x_test,y_train,y_test = utils._split_train_test(features,target)

        model = models._training_best_model(x_train,y_train,x_test,y_test)
        models._make_predictions(model,x_test,y_test)
    except FileNotFoundError:
        logger.error('File not found for {}'.format(filename))

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('filename',
                        help='Filename of covid dataset. For example : covid.csv',
                        type=str)

    args = parser.parse_args()

    main(args.filename)
