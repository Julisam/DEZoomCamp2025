### **📌 Workshop: Data Ingestion with dlt – Homework Solutions**  

This workshop focused on **building scalable data ingestion pipelines** using **dlt** to extract NYC Taxi data from an API, load it into **DuckDB**, and run analytical queries.

---

## **🚀 Solutions & Completed Tasks**  

### **1️⃣ Installing & Checking dlt Version**  
```bash
!pip install dlt[duckdb]
!dlt --version
```
✅ **Answer:** `dlt 1.6.1`  

---

### **2️⃣ Extracting Data Using dlt & API Pagination**  

✅ **Code for Extracting API Data**  
```python
@dlt.resource(name="rides")
def ny_taxi():
    client = RESTClient(
        base_url="https://us-central1-dlthub-analytics.cloudfunctions.net",
        paginator=PageNumberPaginator(
            base_page=1,
            total_path=None
        )
    )

    for page in client.paginate("data_engineering_zoomcamp_api"):  # API endpoint for retrieving taxi ride data
        yield page  # Yield data to manage memory
```
After connecting to the database and running the `DESCRIBE` function, the result shows **4 tables**.  

✅ **Answer:** `4 tables`  

---

### **3️⃣ Checking Total Number of Records**  
```python
len(df)
```
✅ **Answer:** `10000 records`  

---

### **4️⃣ Analyzing Trip Duration**  
Ran the provided SQL query to calculate the **average trip duration in minutes**.  
```python
with pipeline.sql_client() as client:
    res = client.execute_sql(
        """
        SELECT
        AVG(date_diff('minute', trip_pickup_date_time, trip_dropoff_date_time))
        FROM rides;
        """
    )
    print(res)
```
✅ **Answer:** `12.3049 minutes`  

---

## **📩 Submission & Resources**  

📌 **Submission Form:** [🔗 Submit Here](https://courses.datatalks.club/de-zoomcamp-2025/homework/workshop1)  
📌 **GitHub Repository:** Include a link to your GitHub repo containing all code & SQL queries.  

---

## **🛠 Tools & Technologies Used**  
✅ **dlt** – Automating data ingestion  
✅ **DuckDB** – Storing & querying data locally  
✅ **Python** – Extracting, transforming, and analyzing data  
✅ **SQL** – Running analytical queries  

---

## **📂 Repository Structure**  
```
workshop-data-ingestion-dlt/
│
├── ingestion/
│   ├── extract_nyc_taxi_data.py
│   ├── run_pipeline.py
│
├── queries/
│   ├── query_tables_created.sql
│   ├── query_total_records.sql
│   ├── query_trip_duration.sql
│
├── README.md  # This file
```

---

## **📩 Questions or Feedback?**  
If you have any questions or insights, feel free to connect or open an issue in this repository. 🚀  

**⭐ If you found this helpful, don’t forget to star the repo! ⭐**