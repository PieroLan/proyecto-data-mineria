# 🧠 Predicción de Diabetes con Machine Learning

## 📌 Descripción del Proyecto
Este proyecto tiene como objetivo desarrollar un modelo de **clasificación** capaz de predecir la probabilidad de que una persona padezca diabetes, utilizando variables sociodemográficas, clínicas básicas y de estilo de vida.

El enfoque busca demostrar cómo, a partir de datos accesibles (sin pruebas de laboratorio), es posible apoyar la **detección temprana** y la **toma de decisiones en salud pública**.

---

## 🎯 Objetivos

### Objetivo General
Desarrollar un modelo predictivo de diabetes basado en datos reales.

### Objetivos Específicos
- Analizar y procesar datos provenientes de encuestas de salud.
- Identificar variables relevantes para la predicción.
- Construir un modelo de clasificación.
- Evaluar el desempeño del modelo mediante métricas técnicas.

---

## 📊 Dataset

- **Fuente:** INEI (Instituto Nacional de Estadística e Informática)
- **Encuesta:** Encuesta Demográfica y de Salud Familiar (ENDES)
- **Año:** 2024  
- **Módulo:** 1640  
- **Archivo:** `CSALUD01_2024.csv`


---

## 🧾 Variables Utilizadas

### 🧍 Sociodemográficas
- Edad
- Sexo

### ⚕️ Clínicas
- Peso
- Talla
- Perímetro abdominal
- Presión arterial (sistólica y diastólica)
- Diagnóstico de hipertensión

### 🚬 Estilo de Vida
- Consumo de tabaco
- Consumo de alcohol

### 🥗 Alimentación
- Frecuencia de consumo de frutas
- Verduras
- Jugos

---

## ⚙️ Tecnologías Utilizadas

- **Python**
- **Pandas**
- **NumPy**
- Jupyter Notebook

---

## 🔄 Proceso del Proyecto

### 1. Business Understanding
- Definición del problema de clasificación
- Identificación de variables relevantes
- Definición de métricas técnicas y de negocio

### 2. Data Understanding
- Carga de datos
- Exploración inicial (`info()`, `head()`, `shape`)
- Identificación de valores nulos y tipos de datos

### 3. Data Preparation
- Limpieza de datos
- Selección de variables
- Transformación de datos

### 4. Modelado
- Construcción del modelo de clasificación

### 5. Evaluación

Se utilizaron las siguientes métricas:

- **Accuracy ≥ 0.70**
- **Precision ≥ 0.70**
- **AUC-ROC ≥ 0.80**

---

## 📈 Resultados Esperados

- Identificación de personas en riesgo de diabetes sin necesidad de exámenes de laboratorio.
- Apoyo a estrategias de prevención en salud pública.
- Reducción de costos en diagnósticos médicos.

---

## 🚀 Cómo ejecutar el proyecto

1. Clonar el repositorio:
```bash
git clone https://github.com/PieroLan/proyecto-data-mineria.git
```

## 📁 Path del Código en Jupyter

proyecto-data-mineria/
│
├── notebooks/
│   └── proyecto-grupal/
│       └── procesamiento_data_diabetes_sin_transformacion_VF_2.ipynb
│
├── data/
│   └── CSALUD01_2024.csv
│
└── README.md
