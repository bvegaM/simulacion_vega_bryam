import altair as alt
import coloredlogs
import joblib
import logging
logging.basicConfig(level=logging.INFO)
import pandas as pd


from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)
coloredlogs.install()

class Utils:

    def _read_from_csv(self,path):
        logger.info('Reading file for {}'.format(path))
        return pd.read_csv(path)

    def _split_train_test(self,features,target,test_size=0.2):
        logger.info("Split train test values")
        return train_test_split(features,target,test_size=test_size)
    

    def _model_export(self,model,name):
        logger.info("export best model regressor")
        joblib.dump(model,'./models/best_model_{}.pkl'.format(name))

    def _save_df_transform(self,df,name):
        df.to_csv('./out/{}.csv'.format(name),index=False)

    def _save_fig(self,df):
        logger.info("Showing figure test vs predictions")
        a = alt.Chart(df).mark_point(size=40,opacity=0.5,color='orange').encode(
            x='day',
            y='y'
        )
        b = alt.Chart(df).mark_line(color='red').encode(
            x='day',
            y=alt.Y('y_pred',axis=alt.Axis(title='confirmed'))
        )

        chart =(a+b).properties(title='Train vs predictions').interactive()
        chart.show()

