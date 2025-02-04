## Homework 2: 02-Workflow-Orchestration-with-Kestra

Welcome to **Week 2** of the **Data Engineering Zoomcamp**! This week focuses on Workflow Orchestration, using Kestra to automate data pipelines and manage ETL workflows efficiently. The homework extends the existing workflow to process additional data while answer some qestions related to the workflow orchestration.

---

## 📋 **Assignment Overview**  

During the course, we processed green and yellow NYC taxi data for the year 2019. The assignment is to extend the existing workflows to include data for subsequent dates. To do that, we use the Kestra’s **backfill functionality** and **subflows** to automate processing for both **Yellow** and **Green** taxi datasets.

---

## 📝 **Quiz Answers**  

### **1️⃣ Uncompressed File Size for December 2020 (Yellow Taxi Data)**  
✅ **Answer:** `128.3 MB`  

### **2️⃣ Rendered Value of `file` Variable (Green Taxi, April 2020)**  
✅ **Answer:** `green_tripdata_2020-04.csv`  

### **3️⃣ Total Rows in Yellow Taxi Data (2020)**  
✅ **Answer:** `24,648,499`  

### **4️⃣ Total Rows in Green Taxi Data (2020)**  
✅ **Answer:** `1,734,051`  

### **5️⃣ Total Rows in Yellow Taxi Data (March 2021)**  
✅ **Answer:** `1,925,152`  

### **6️⃣ Configuring New York Timezone in Kestra Schedule**  
✅ **Answer:** `Add a timezone property set to America/New_York in the Schedule trigger configuration`  

---

## 🛠 **Tools Used**  

- **Kestra** → Workflow orchestration  
- **BigQuery** → Data warehouse for storing and analyzing data  
- **Google Cloud Storage (GCS)** → Cloud-based data lake  
- **Docker & Docker Compose** → Local environment setup  
