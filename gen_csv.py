# Patras Ionut-Marcelin 311CB

import pandas as pd
import numpy as np
# import random

# setam un seed pentru reproductibilitate
np.random.seed(42)

# parametrii datasetului
n_total = 1000  # 700 train + 300 test

# generam coloanele
greutate = np.random.triangular(left=800, mode=1300, right=2500, size=n_total)
greutate = greutate.astype(int)
dimensiunea_motorului = np.random.triangular(left=800, mode=1400 ,right=5000, size=n_total)
dimensiunea_motorului = dimensiunea_motorului.astype(int)
putere_cp = np.random.triangular(left=50,mode = 115, right=350, size=n_total)
putere_cp = putere_cp.astype(int)
transmisie = np.random.choice(['manuala', 'automata'], size=n_total, p=[0.63,0.37])
tip_combustibil = np.random.choice(['benzina', 'motorina', 'hibrid'], size=n_total, p=[0.43,0.37,0.20])
caroserie = np.random.choice(['hatchback', 'sedan', 'SUV', 'combi', 'coupe'], size=n_total)
an_fabricatie = np.random.randint(1998, 2025, size=n_total)

# simulam consumul in functie de alti factori
# formula simplificata: valori mai mari la greutate, motor si putere => consum mai mare;
# hibridele consuma mai putin
consum_baza = (
    5.5 +
    (greutate - 1020) / 1000 * 4 +
    (dimensiunea_motorului - 800) / 4200 * 6 +
    (putere_cp - 70) / 250 * 4
)

# ajustare in functie de combustibil
consum_baza += np.where(tip_combustibil == 'hibrid', -2.0, 0.0)
consum_baza += np.where(tip_combustibil == 'motorina', -0.5, 0.0)

# adaugam putin zgomot
consum = consum_baza + np.random.normal(0, 0.8, size=n_total)
consum = np.round(consum, 2)

# construim DataFrame-ul final
df = pd.DataFrame({
    'Greutate_kg': greutate,
    'DimensiuneaMotorului_cm3': dimensiunea_motorului,
    'Putere_CP': putere_cp,
    'Transmisie': transmisie,
    'Tip_Combustibil': tip_combustibil,
    'Caroserie': caroserie,
    'An_Fabricatie': an_fabricatie,
    'Consum_L_100km': consum
})

# impartim in train si test
df_train = df.sample(n=700, random_state=42)
df_test = df.drop(df_train.index)

# salvam CSV-urile
train_path = "train.csv"
test_path = "test.csv"

df_train.to_csv(train_path, index=False)
df_test.to_csv(test_path, index=False)

train_path, test_path