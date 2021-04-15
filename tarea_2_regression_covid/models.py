import coloredlogs
import logging
logging.basicConfig(level=logging.INFO)
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter("ignore")


from utils import Utils

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

logger = logging.getLogger(__name__)
coloredlogs.install()
utils = Utils()

class Model:

    def __init__(self):
        self.reg = {
            'LINEAR': LinearRegression(fit_intercept=True),
            'POLYNOMIAL': Pipeline([('poly', PolynomialFeatures(degree=4)),
                         ('linear', LinearRegression(fit_intercept=False))])
        }

    def _training_best_model(self,x_train,y_train,x_test,y_test):
        logger.info("================ Starting training regerssor model ================")
        best_score = 0
        best_model = None
        best_name_model = ''

        for name,reg in self.reg.items():
            logger.info("Training with {} model".format(name))
            
            model = reg.fit(x_train,y_train)
            score= np.abs(model.score(x_test,y_test))
            if score > best_score:
                best_score = score
                best_model = model
                best_name_model = name

        logger.info("Best model is {name} with score {score}".format(name=best_name_model,score=best_score))
        
        utils._model_export(best_model,best_name_model)
        return best_model

    def _make_predictions(self,model,x_test,y_test):
        logger.info("Make predictions and save data")
        data=pd.DataFrame({'day':x_test.reshape(-1),'y':y_test.reshape(-1),'y_pred':model.predict(x_test).reshape(-1)})
        utils._save_df_transform(data,'predictions')
        utils._save_fig(data)
        
        