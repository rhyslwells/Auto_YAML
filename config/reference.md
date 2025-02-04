# Overview

This reference guides automatic YAML metadata generation, ensuring consistency in:

- Tags: Keywords for topic classification.
- Category: High-level classification.
- Phase: Machine Learning Workflow phase.
- Topic: Specific subject within the phase.
- Filename: Standardized naming format.


### **`reference.md` (Optimized for YAML Generation)**  

## **1. Metadata Generation Format**  
For any given note, extract:  
- **Tags** (at least two).  
- **Category**.  
- **Phase, Topic, and Filename** based on content.  

**Output Example:**  
```yaml
---
tags: 
  - data_storage
  - big_data
aliases:
category: DATA_ANALYSIS
phase: Model Selection
topic: Parquet File Handling
filename: parquet_file_handling.py
---
```

## **2. Overview**  
This reference guides **automatic YAML metadata generation**, ensuring consistency in:  
- **Tags**: Keywords for topic classification.  
- **Category**: High-level classification.  
- **Phase**: Machine Learning Workflow phase.  
- **Topic**: Specific subject within the phase.  
- **Filename**: Standardized naming format.  

## **3. Categories & Tags**  
| **Category**            | **Relevant Tags**                                                               |
|-------------------------|--------------------------------------------------------------------------------|
| **Data Science (DS)**   | #classifier, #regressor, #evaluation, #clustering, #deep_learning, #anomaly_detection |
| **MLOps**               | #ml_process, #ml_optimisation, #model_explainability                          |
| **Language Models**     | #GenAI, #language_models, #NLP                                                |
| **Data Engineering (DE)** | #database, #data_storage, #data_modeling, #data_cleaning, #data_exploration |
| **DevOps**              | #software, #data_orchestration, #software_architecture                        |
| **Data Analysis (DA)**  | #data_visualization                                                           |
| **Mathematics**         | #statistics, #math                                                            |
| **Career**             | #career, #energy                                                              |


## **4. Tag Definitions**  
| **Tag**                 | **Meaning**                                                 |
|-------------------------|-------------------------------------------------------------|
| **#classifier**         | Predicts categories or labels.                              |
| **#regressor**          | Predicts continuous values.                                 |
| **#evaluation**         | Measures model performance.                                 |
| **#clustering**         | Groups similar data points.                                |
| **#deep_learning**      | Uses multi-layered neural networks.                        |
| **#ml_process**         | Covers ML model development and deployment.                |
| **#ml_optimisation**    | Improves ML model performance.                             |
| **#data_storage**       | Methods for storing and managing data.                     |
| **#database**           | Structured data collection.                                |


## **5. Machine Learning Workflow Phases**  
| **Phase**              | **Description**                     |
|------------------------|-------------------------------------|
| **Preprocessing**      | Data cleaning & transformation.    |
| **Model Building**     | Training machine learning models.  |
| **Model Selection**    | Choosing the best model.           |
| **Optimisation**       | Tuning hyperparameters.            |
| **Deployment**         | Serving models in production.      |
| **Observability**      | Monitoring performance.            |


## **6. Filename & Path Generation**  
Use **ML workflow phases** to determine file naming:

```
https://github.com/rhyslwells/ML_Tools/{phase}/{topic}/{filename}.py
```

Example:  
```
https://github.com/rhyslwells/ML_Tools/Model_Selection/Parquet_File_Handling/parquet_file_handling.py
```

