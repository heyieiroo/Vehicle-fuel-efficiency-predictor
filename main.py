# Patras Ionut-Marcelin 311CB

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from math import sqrt
import numpy as np

# incarcam datele
train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

def Analiza_Exploratorie(dataset, titlu):
    print(f"\n{titlu.upper()} SET")
    # Mic titlu
    
    # Valori lipsa
    print("\nValori lipsa (numar):\n", dataset.isnull().sum())
    print("\nValori lipsa (%):\n", 100 * dataset.isnull().mean())
    # Obs: nu exista valori lipsa => nu e necesara imputare

    # Statistici descriptive
    print("\nStatistici descriptive - numerice:\n", dataset.describe())
    print("\nStatistici descriptive - categorice:\n", dataset.describe(include=['object']))

    # Distributia variabilelor
    col_numerice = ['Greutate_kg', 'DimensiuneaMotorului_cm3', 'Putere_CP', 'An_Fabricatie', 'Consum_L_100km']
    col_categorice = ['Transmisie', 'Tip_Combustibil', 'Caroserie']

    for col in col_numerice:
        plt.figure()
        sns.histplot(dataset[col], kde=True, bins=30)
        plt.title(f"Distributie: {col}")
        plt.show()
        # Obs: Distributia e normala / asimetrica

    for col in col_categorice:
        plt.figure()
        sns.countplot(x=dataset[col])
        plt.title(f"Frecventa: {col}")
        plt.show()
        # Comentariu: Verificăm dacă distribuția pe categorii este echilibrată

    # Detectare outlieri
    for col in col_numerice:
        plt.figure()
        sns.boxplot(x=dataset[col])
        plt.title(f"Boxplot pentru {col}")
        plt.show()
        # Obs: valorile situate in afara whisker-ului pot fi considerate outlieri

    # Heatmap corelatii (Matricea de corelatii)
    plt.figure(figsize=(10, 8))
    sns.heatmap(dataset[col_numerice].corr(), annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Matrice corelatii variabile numerice")
    plt.show()
    # Obs: Identificam care variabile numerice influenteaza consumul

    # Relatii cu variabila tinta (consumul)
    for col in col_numerice:
        if col != 'Consum_L_100km':
            plt.figure()
            sns.scatterplot(x=dataset[col], y=dataset['Consum_L_100km'])
            plt.title(f"{col} vs Consum")
            plt.show()
            # Obs: Vizualizam relatia lineara cu tinta

    for col in col_categorice:
        plt.figure()
        sns.violinplot(x=dataset[col], y=dataset['Consum_L_100km'])
        plt.title(f"{col} vs Consum")
        plt.show()
        # Obs: Comparam distributia consumului în functie de fiecare categorie

# Rulam EDA pe ambele subseturi
Analiza_Exploratorie(train, "Train")
Analiza_Exploratorie(test, "Test")


# Pregatire date pt model
X_train = train.drop(columns=['Consum_L_100km'])
y_train = train['Consum_L_100km']
X_test = test.drop(columns=['Consum_L_100km'])
y_test = test['Consum_L_100km']

cat_feat = ['Transmisie', 'Tip_Combustibil', 'Caroserie']
num_feat = ['Greutate_kg', 'DimensiuneaMotorului_cm3', 'Putere_CP', 'An_Fabricatie']

# Encoder categorice
prep = ColumnTransformer([
    ('cat', OneHotEncoder(drop='first'), cat_feat)
], remainder='passthrough')

# Pipeline cu regresie
pipe = Pipeline([
    ('prep', prep),
    ('lr', LinearRegression())
])

pipe.fit(X_train, y_train)
preds = pipe.predict(X_test)

# Scoruri model
print("\nMAE:", mean_absolute_error(y_test, preds))
print("RMSE:", sqrt(mean_squared_error(y_test, preds)))
print("R2:", r2_score(y_test, preds))

# Grafic predictii
plt.scatter(y_test, preds)
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], 'r--')
plt.xlabel("Real")
plt.ylabel("Prev")
plt.title("Real vs Prev")
plt.show()
