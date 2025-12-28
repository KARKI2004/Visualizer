# CMPS 3400 Used Car Data Science Project  
**Authors:** Samiksha Gnawali & Suyog Karki  
**Instructor:** Dr. Omer M. Soysal  
**Course:** CMPS 3400 Introduction to Data Science  

---

## Overview
Visualizer is a Python-based data analysis tool that demonstrates:
- CSV and pickle analysis with interactive visualization  
- Probability tables, vector operations, and correlation analysis  
- Missing-value handling, downloads, and logging  

Technologies used: **Pandas**, **Matplotlib**, **Seaborn**, **NumPy**, **Streamlit**

---

## Setup
```
git clone https://github.com/KARKI2004/CMPS_3400_Project.git
cd CS340_F_25_Mango
pip install pandas matplotlib seaborn numpy streamlit
```

## Run (CLI)
```
python CS340_Project/main.py
```

## Run (UI)
```
streamlit run app.py
```

## Outputs
- CLI run writes analysis outputs and plots to `Output/`
- UI run provides download buttons and does not write to disk

## Deploy (Google Cloud Run)
1) Build and push the container:
```
gcloud builds submit --tag gcr.io/<PROJECT_ID>/visualizer
```
2) Deploy:
```
gcloud run deploy visualizer --image gcr.io/<PROJECT_ID>/visualizer --platform managed --region <REGION> --allow-unauthenticated
```
