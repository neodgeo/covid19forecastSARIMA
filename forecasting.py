def forecastOneToStep(covid19_france_df):
    import pylab
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    from sklearn.metrics import mean_squared_error
    from numpy.linalg import LinAlgError
    from math import sqrt
    import pandas as pd
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import statsmodels
    import sys
    import pmdarima as pm

    dates = [pd.datetime.strptime(x, '%m/%d/%y') for x in list(covid19_france_df.columns[1:])]
    values = list((covid19_france_df.values)[0][1:])
    values = np.sort(values)
    values = values.tolist()
    serie_temporelle = pd.Series(values,index=dates)
    serie_temporelle.index.name = 'date'

    meilleur_modele_SARIMAX = [(0,1,0),(1,1,0,12)]


    X = serie_temporelle.values
    X = [x for x in X if x > 0]

    taille_train_data = int(len(X) * 0.66)
    print("Taille du dataset de test=",len(X)-taille_train_data)

    train_data, test_data = X[0:taille_train_data], X[taille_train_data:len(X)]
    predictions_SARIMAX = {}
    print("*"*90)

    drapeau_erreur = False
    print("Modèle SARIMAX:",meilleur_modele_SARIMAX)
    historique = [x for x in train_data]
    predictions = list()
    nbr_predictions = 1 #Choix du nombre de jour de prédiction dans le futur
    nbr_jours_init = len(X)-len(test_data)

    for t in range(len(test_data)+nbr_predictions):
        modele_SARIMAX = SARIMAX(historique, order=meilleur_modele_SARIMAX[0],seasonal_order=meilleur_modele_SARIMAX[1],enforce_stationarity=False)
        modele_SARIMAX_entraine = modele_SARIMAX.fit(disp=0)
        sortie = modele_SARIMAX_entraine.forecast()
        predict = sortie[0]
        predictions.append(predict)
        if t < len(test_data):
            vraie_valeur = test_data[t]
            historique.append(vraie_valeur)
            print('Nombre de jours écoulés=%i, t=%i, prédiction=%i, Valeur mesurée=%i' % (nbr_jours_init+t,t,predict,vraie_valeur))
        else:
            historique.append(predict)
            print("Meilleur_SARIMAX",meilleur_modele_SARIMAX)
            etiq_SARIMAX = "_".join([str(hyperparam) for hyperparam in meilleur_modele_SARIMAX])
            if not etiq_SARIMAX in predictions_SARIMAX.keys():
                predictions_SARIMAX[etiq_SARIMAX]=int(predict)
            print('Nombre de jours écoulés=%i, t=%i, prédiction=%i' % (nbr_jours_init+t,t,predict))

    
    predictDate = (dates[-1]+pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    dates.append(predictDate)
    values.append(int(historique[-1]))
    df = pd.DataFrame(list(zip(dates,values)),columns=['date','values'])
    df['date'] = df['date'].astype(str)

    df_case = df.copy()
    previous_val = ''
    for index, val in enumerate(df_case['values']):
        if index == 0:
            previous_val = val
            continue
        case_val = val - previous_val
        df_case['values'][index] = case_val
        previous_val = val
    return df, df_case