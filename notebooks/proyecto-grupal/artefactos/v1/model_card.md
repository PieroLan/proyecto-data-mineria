# Model Card — CAT
**Versión:** v1  
**Sistema:** Python 3.12.7, scikit-learn 1.5.1

## Datos
Archivo: `data_preparada.csv` | Shape: (2379, 13) | Objetivo: `QS109_F` (NOTIENE=0, TIENE=1) | Prevalencia: 0.454

## Entrenamiento
Split 80/20 estratificado (random_state=42). Preprocesamiento: StandardScaler (num) + OneHotEncoder(ignore) (cat) + SMOTE(k=3).

## Modelo
Seleccionado para TEST: **CAT**.  
Umbral de decisión: **0.50** (provisional).

## Métricas en TEST
F1=0.712, P=0.693, R=0.731,
ROC-AUC=0.815, PR-AUC=0.781.
