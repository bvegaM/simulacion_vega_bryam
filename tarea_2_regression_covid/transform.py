import coloredlogs
import logging
logging.basicConfig(level=logging.INFO)
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)
coloredlogs.install()

from utils import Utils

class Transform:

    def __init__(self,df,feautres,target):
        try:
            self._df = df.copy(deep=True)
            self._features = feautres
            self._target = target
        except KeyError:
            logger.error("Column not found")
        

    def _transform_process(self):
        logger.info("================ Starting transform dataset process ================")
        self._obtain_features_target()
        return self._features,self._target


    def _obtain_features_target(self):
        logger.info("Obtain feautres and target")
        self._features = self._df.iloc[:,self._features-1:self._features].values
        self._target = self._df.iloc[:,self._target-1:self._target].values




    
    