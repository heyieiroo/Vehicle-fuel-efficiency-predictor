# Construirea si explorarea unui dataset tabelar

Tema abordata este o **problema de regresie**, in care ne propunem sa prezicem **consumul (L/100km) al unei masini** pe baza unor caracteristici tehnice si structurale.

<p align="center">
  <img src="images/0.png" alt="0" width="500">
</p>

Am optat pentru generarea sintetica a datelor. Setul de date simuleaza caracteristici reale ale unor autoturisme:
- Greutate (kg)
- Dimensiunea motorului (cm³)
- Putere (CP)
- Tip transmisie (automata, manuala)
- Tip combustibil (benzina, motorina, hibride)
- Tip caroserie
- An fabricatie
- Consum estimat (variabila tinta)

## Observatii
- Codul este impartit in 2 fisiere diferite:
  - `gen_csv.py` ce genereaza propriu-zis fisierele `train.csv` si `test.csv`
  - `main.py` care contine EDA-ul si Antrenarea modelului
- Greutatea, puterea si dimensiunea motorului au fost generate folosind o distributie triangulara, concentrata spre valori mai mici, reflectand faptul ca majoritatea masinilor de pe piata sunt modele compacte sau medii.
- Consumul a fost calculat ca o funcție neliniară de greutate, motor, putere și combustibil, cu puțin zgomot aleator.
- Setul a fost impartit in:
  - `train.csv` – 700 exemple
  - `test.csv` – 300 exemple

---

## Analiza exploratorie a datelor

### Statistici descriptive
<p align="center">
  <img src="images/1-2.png" alt="1-2" width="500">
</p>

- Valorile variabilelor numerice sunt distribuite realist.
- Distributiile pentru variabile categorice sunt echilibrate, dar reflecta diversitate.

### Analiza distributiei variabilelor
<p align="center">
  <img src="images/3.png" alt="3" width="500">
</p>
<p align="center">
  <img src="images/4.png" alt="4" width="500">
</p>

- Histogramele arata asimetrie la “Greutate”, “Putere_CP” și “Dimensiunea Motorului”, asa cum am intentionat.
- Distribuția consumului este moderat normala, cu usoara intindere spre valorile mari.
- Se observa diferenta numerelor de exemplare pe motorina fata de benzina, la fel si cele manuale fata de cele automate.

### Detectarea outlierilor
<p align="center">
  <img src="images/5.png" alt="5" width="500">
</p>

- Exista cativa outlieri la “Putere_CP” și “Consum_L_100km”, dar acestia reflecta cazuri realiste (ex: SUV-uri puternice).

### Analiza corelatiilor
<p align="center">
  <img src="images/6.png" alt="6" width="500">
</p>

- Cea mai mare corelație cu consumul o au: “DimensiuneaMotorului” și “Greutate”.

### Analiza relatiilor cu variabila tinta
<p align="center">
  <img src="images/7.png" alt="7" width="500">
</p>

- Variabilele `Putere_CP`, `Greutate` și `Motor` cresc consumul.

<p align="center">
  <img src="images/8.png" alt="8" width="500">
</p>
<p align="center">
  <img src="images/9.png" alt="9" width="500">
</p>

- Masinile hibride au un consum evident mai mic (vizibil în graficele de tip violin plots).

---

## Antrenarea si evaluarea unui model de baza

A fost folosita Regresia Liniara din biblioteca Sklearn.

<p align="center">
  <img src="images/10.png" alt="10" width="500">
</p>

**Performantele modelului:**
- **MAE:** 0.6975887403249262
- **RMSE:** 0.8770958163161408
- **R2:** 0.8829641574855024