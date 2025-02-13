## Homework 3: 03-Data-Warehousing-with-BigQuery


Welcome to **Week 3** of the **Data Engineering Zoomcamp**! This week, we explored **Data Warehousing** concepts and **BigQuery** best practices. The homework involved working with **Yellow Taxi Trip Records (Jan–June 2024)**, focusing on **external tables, query performance, partitioning, clustering, and cost optimization**.

---

## **🚀 Tasks Completed & Solutions**  

### **1️⃣ Create an External Table in BigQuery**  
The **external table** is created using **PARQUET format** from data stored in **Google Cloud Storage (GCS)**.  
```sql
CREATE OR REPLACE EXTERNAL TABLE module-3-data-warehouse.taxi_data_eu10.external_yellow_tripdata_2024 
OPTIONS ( 
  format = 'PARQUET',
  uris = ['gs://module3-dez-sss/yellow_tripdata_2024-*.parquet']
);
```

---

### **2️⃣ Create a Regular (Materialized) Table in BigQuery**  
This table is **fully managed by BigQuery** and allows for **faster querying** compared to an external table.  
```sql
CREATE OR REPLACE TABLE module-3-data-warehouse.taxi_data_eu10.your_regular_table_name AS 
SELECT * FROM module-3-data-warehouse.taxi_data_eu10.external_yellow_tripdata_2024;
```

---

### **3️⃣ Querying & Data Analysis**  

#### **📊 Question 1: Record Count in Yellow Taxi Data (Jan–June 2024)**  
```sql
SELECT COUNT(*) FROM module-3-data-warehouse.taxi_data_eu10.your_regular_table_name;
```
✅ **Answer:** `20,332,093` records  

---

#### **📊 Question 2: Counting Distinct PULocationIDs & Data Read Estimates**  
```sql
SELECT COUNT(DISTINCT PULocationID) FROM module-3-data-warehouse.taxi_data_eu10.external_yellow_tripdata_2024;
SELECT COUNT(DISTINCT PULocationID) FROM module-3-data-warehouse.taxi_data_eu10.your_regular_table_name;
```
✅ **Answer:**  
- **External Table:** `0 MB`  
- **Materialized Table:** `155.12 MB`  

---

#### **📊 Question 3: Why Does Querying Two Columns Require More Bytes?**  
```sql
SELECT PULocationID FROM module-3-data-warehouse.taxi_data_eu10.your_regular_table_name;
SELECT PULocationID, DOLocationID FROM module-3-data-warehouse.taxi_data_eu10.your_regular_table_name;
```
✅ **Answer:**  
BigQuery is a **columnar database**, meaning it only scans the requested columns. Querying **two columns (PULocationID, DOLocationID)** requires reading **more data** than a single column (PULocationID), leading to a higher **estimated bytes processed**.  

---

#### **📊 Question 4: Number of Records with `fare_amount = 0`**  
```sql
SELECT COUNT(*) FROM module-3-data-warehouse.taxi_data_eu10.your_regular_table_name WHERE fare_amount = 0;
```
✅ **Answer:** `8,333` records  

---

### **4️⃣ Optimizing Table Performance in BigQuery**  

#### **📊 Question 5: Best Strategy for Partitioning & Clustering**  
✅ **Strategy:** Partition by `tpep_dropoff_datetime` and Cluster on `VendorID`.  

```sql
CREATE OR REPLACE TABLE module-3-data-warehouse.taxi_data_eu10.optimized_yellow_tripdata_2024 
PARTITION BY DATE(tpep_dropoff_datetime) 
CLUSTER BY VendorID AS 
SELECT * FROM module-3-data-warehouse.taxi_data_eu10.your_regular_table_name;
```

✅ **Why?**  
- **Partitioning** improves **query performance** by **reducing the amount of scanned data**.  
- **Clustering** optimizes queries that **filter by `VendorID`**.  

---

### **5️⃣ Querying VendorIDs with Partitioned & Non-Partitioned Tables**  

```sql
SELECT DISTINCT VendorID 
FROM module-3-data-warehouse.taxi_data_eu10.your_regular_table_name 
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';

SELECT DISTINCT VendorID 
FROM module-3-data-warehouse.taxi_data_eu10.optimized_yellow_tripdata_2024 
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
```
✅ **Answer:**  
- **Non-Partitioned Table:** `310.24 MB`  
- **Partitioned Table:** `26.84 MB`  

🚀 **Partitioning reduced the bytes read significantly!**  

---

### **6️⃣ Additional Questions**  

#### **📊 Question 7: Where is the External Table Data Stored?**  
✅ **Answer:** **GCP Bucket**  

#### **📊 Question 8: Should You Always Cluster Data in BigQuery?**  
✅ **Answer:** **False**  
- Clustering is **not always necessary**—it **depends on query patterns and table size**.  

#### **📊 Question 9: Estimated Bytes for `SELECT COUNT(*)` Query**  
```sql
SELECT COUNT(*) FROM module-3-data-warehouse.taxi_data_eu10.your_regular_table_name;
```
✅ **Answer:** `0 MB`  
- BigQuery optimizes `COUNT(*)` queries by using **metadata instead of scanning rows**, making it highly efficient.  

---

## **🛠 Tools & Technologies Used**  
✅ **Google Cloud Storage (GCS)** – Storing Parquet files  
✅ **BigQuery** – Querying & data analysis  
✅ **Parquet Format** – Optimized storage for efficiency  
✅ **SQL** – Running analytical queries  
