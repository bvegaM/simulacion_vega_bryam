import argparse
import coloredlogs
import logging
import numpy as np
import os
import pandas as pd

from transform import  Transform
from utils import Utils

logger =  logging.getLogger(__name__)
coloredlogs.install()

def main(files):
    logger.info("Starting transform and merging process to {}".format(files))

    list_data_frames= []
    utils = Utils()

    for i in files:
        logger.info("Transform process to {}".format(os.path.basename(i)))

        key = os.path.basename(i).replace('.csv','')
        transform = Transform(i,['year',os.path.basename(i).replace('.csv','_value')])
        df = transform._transform_process()
        list_data_frames.append(df)

    df = transform._merge_data(list_data_frames,'year')
    df.dropna(inplace=True)
    
    utils._export_transform_dataset(df)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('files',
                        help='Data to transform and merge, separate with comma example:python main.py  in/pib.csv,in/gasto.csv,in/inversion.csv,in/exportacion.csv,in/importacion.csv',
                        type=str)

    args = parser.parse_args()

    main([i for i in args.files.split(',')])
