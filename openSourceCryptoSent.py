import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_absolute_error
import statsmodels.api as sm
from datetime import datetime, timedelta
import seaborn as sns
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

sentimentComponent = pd.read_csv("/Volumes/Research/Crypto_Factors_Project/sentiment score/comprehensive sentiment/component_origins.csv", index_col=0)
sentimentComponent.fillna(0, inplace=True)

sentimentComponent["crypto_index_lag"] = sentimentComponent["crypto_index"].shift()
sentimentComponent["volatility_lag"] = sentimentComponent["volatility"].shift()
sentimentComponent["google trends_lag"] = sentimentComponent["google trends"].shift()
sentimentComponent["total count_lag"] = sentimentComponent["total count"].shift()
sentimentComponent["dollarVolume_lag"] = sentimentComponent["dollarVolume"].shift()
sentimentComponent["address #_lag"] = sentimentComponent["address #"].shift()
sentimentComponent["blockUsd_lag"] = sentimentComponent["blockUsd"].shift()
sentimentComponent["ico_lag"] = sentimentComponent["ico"].shift()
sentimentComponent.fillna(0, inplace=True)


scaler = StandardScaler()
scaled_df = sentimentComponent[['crypto_index_lag', 'google trends',
                                'total count_lag', 'volatility', 'dollarVolume_lag', 
                                "address #", "blockUsd_lag", "ico"]].copy()
scaled_df = pd.DataFrame(scaler.fit_transform(scaled_df), columns=scaled_df.columns)
pca = PCA(n_components=1, svd_solver='auto')
Principal_components=pca.fit_transform(scaled_df)
pca_df = pd.DataFrame(data = Principal_components, columns = ['bestRatio'])

# print(pca.components_)
sentimentScore = sentimentComponent.merge(pca_df['bestRatio'], left_index=True, right_index=True)
sentimentScore = sentimentScore[['date', 'bestRatio']].rename(columns={'bestRatio': 'sentimentScore'}, inplace=False)
sentimentScore.to_csv("./sentiment score.csv")