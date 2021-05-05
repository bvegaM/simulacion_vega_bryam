import papermill as pm

pm.execute_notebook(
    'input.ipynb',
    'output.ipynb',
    parameters = dict(path_confirmed='./in/time_series_covid19_confirmed_global.csv',
                    path_recovered='./in/time_series_covid19_recovered_global.csv',
                    country='Ecuador',
                    date='3/1/20')
)
