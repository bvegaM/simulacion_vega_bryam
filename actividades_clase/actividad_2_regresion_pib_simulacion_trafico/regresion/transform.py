import pandas as pd
import numpy as np

from functools import reduce

class Transform:

    def __init__(self,path,columns_name):
        self._path = path
        self._columns_name = columns_name
        self._df=None

    def _transform_process(self):
        self._df = self._read_csv()
        self._obtain_year_value()
        self._convert_dtype_data()
        return self._df


    def _merge_data(self,data,key):
        return reduce(lambda  left,right: pd.merge(left,right,on=[key],
                                            how='inner'), data)


    def _convert_dtype_data(self):
        self._df[self._columns_name[0]] = self._df[self._columns_name[0]].astype(np.int64)
        if type(self._df[self._columns_name[1]].values[0]) not in (np.int, np.float, np.long, np.complex):
            self._df[self._columns_name[1]] = self._df[self._columns_name[1]].apply(lambda x: x.replace(',','.')).astype(np.float64)
        else:
            self._df[self._columns_name[1]] = self._df[self._columns_name[1]].astype('str')
            self._df[self._columns_name[1]] = np.abs(self._df[self._columns_name[1]].apply(lambda x: x.replace(',','.')).astype(np.float64))

    def _obtain_year_value(self):
        self._df = self._df[self._df['Country/Region']=='Ecuador']
        self._df = pd.DataFrame(self._df.iloc[0].loc['1960':])
        self._df.reset_index(inplace=True)
        self._df.columns = self._columns_name

    def _read_csv(self):
        return pd.read_csv(self._path,sep=";")
