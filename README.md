# Network Security Project

This project is a **machine learning–based Network Security application**. It can **train a model** and **predict whether network data is safe or malicious** using a web API built with **FastAPI**.

Below is the complete workflow explained in **simple language**.

---

## 1. Project Startup

When the project starts:

* Environment variables are loaded using `.env` file (for MongoDB URL).
* A secure connection to **MongoDB** is created.
* A **FastAPI web server** is started.

The API is accessible through a browser.

---

## 2. MongoDB Connection

* The project connects to MongoDB using a URL stored in an environment variable.
* MongoDB is used to **store raw and processed network data** during training.
* Database and collection names are taken from constant files to keep things organized.

---

## 3. API Endpoints (Main Features)

### (a) Home Route `/`

* Redirects the user to FastAPI documentation (`/docs`).
* Useful for testing APIs easily.

---

### (b) Training Route `/train`

**Purpose:** Train the machine learning model.

**What happens internally:**

1. `TrainingPipeline` object is created.
2. The training pipeline runs step-by-step:

   * Data ingestion (fetching data)
   * Data validation
   * Data transformation
   * Model training
   * Model evaluation
   * Model saving
3. Final trained model and preprocessor are stored in the `final_model/` folder.

**Output:**

* A success message once training is completed.

---

### (c) Prediction Route `/predict`

**Purpose:** Predict results for new network data.

**Input:**

* A CSV file uploaded by the user.

**Workflow:**

1. Uploaded CSV file is read using Pandas.
2. Saved **preprocessor** is loaded from `preprocessor.pkl`.
3. Saved **trained model** is loaded from `model.pkl`.
4. Both are combined using `NetworkModel`.
5. Predictions are made on the uploaded data.
6. A new column (`predicted_column`) is added to the data.
7. Output is:

   * Saved as a CSV file (`prediction_output/output.csv`)
   * Displayed as an HTML table in the browser

**Output:**

* Prediction results shown in a table format.

---

## 4. Machine Learning Model Handling

* `preprocessor.pkl` → Handles data scaling/encoding
* `model.pkl` → Trained ML model
* `NetworkModel` → Combines preprocessing + prediction into one step

This makes prediction easy and clean.

---

## 5. Error Handling & Logging

* Custom exception class `NetworkSecurityException` is used.
* Errors are logged properly for debugging.
* If prediction fails, error details are returned clearly.

---

## 6. Frontend (HTML Output)

* Predictions are shown using **Jinja2 templates**.
* Data is displayed as a clean table in the browser.

---

## 7. Overall Flow Summary

```
User → Upload CSV / Trigger Training
     → FastAPI
     → ML Pipeline / Model
     → Prediction
     → CSV + Table Output
```

---

## 8. Technologies Used

* Python
* FastAPI
* MongoDB
* Machine Learning
* Pandas

---

