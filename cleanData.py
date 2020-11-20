def cleanDataToDF():
    import pandas as pd

    path = 'COVID-19/csse_covid_19_data/csse_covid_19_time_series/'
    covid19_dataset_df = pd.read_csv(path+'time_series_covid19_confirmed_global.csv',sep=',')
    covid19_dataset_df = covid19_dataset_df.drop(['Lat', 'Long'],axis='columns')
    covid19_dataset_df = covid19_dataset_df.groupby(['Country/Region']).sum().reset_index()
    covid19_france_df = covid19_dataset_df[covid19_dataset_df['Country/Region']=="France"]

    return covid19_france_df