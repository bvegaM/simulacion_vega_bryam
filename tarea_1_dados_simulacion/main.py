import argparse
import coloredlogs
import datetime
import logging
logging.basicConfig(level=logging.INFO)
import pandas as pd
import numpy as np
import os

from model.dices import Dice

logger =  logging.getLogger(__name__)
coloredlogs.install()

def main(list_simulate):
    logger.info("Starting simulate to {}".format(list_simulate))

    try:
        os.mkdir('figures')
    except:
        logger.error('Creation of the directory {} failed'.format('figures'))

    for i in list_simulate:
            df = pd.DataFrame({'sum':_simulate_sum(i)})
            _generate_histogram(df,'figure_size_{}'.format(i),i)
        

def _simulate_sum(size):
    logger.info("Simulate Dice sum with size of {}".format(size))

    dice_one = Dice()
    dice_two = Dice()
    frequency = [dice_one._throw_dice()+dice_two._throw_dice() for i in range(0,size)]
    return frequency


def _generate_histogram(df,name_figure,size):
    logger.info("Generating Histograme for {}".format(name_figure))
    
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    hist = df.plot(kind='hist',figsize=(10,7),bins=11,
                    alpha=0.7,color='yellowgreen',grid=True,
                    title='Frequency of addition of two dice for a test of {} values'.format(size))
    fig = hist.get_figure()
    fig.savefig('figures/{name}_{date}_histogram.png'.format(name=name_figure,date=now))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('list_simulate',
                        help='List of values to simulate. For example : python main.py 10,100',
                        type=str)
    args = parser.parse_args()

    main([int(i) for i in args.list_simulate.split(',')])

