import joblib
from sklearn.model_selection import  train_test_split

class Utils:

    def _obtain_feature_target(self,df,target_name,feature_name):
        feature = df[feature_name]
        target = df[target_name]
        return feature,target

    def _obtain_train_test(self,feature,target,test_size=0.2):
        return train_test_split(feature,target,test_size=test_size)

    def _export_model(self,model):
        joblib.dump(model,'./models/model_pib.pkl')

    def _export_transform_dataset(self,df):
        df.to_csv('./out/pib_dataset.csv',index=False)
