## Homework 4: 04-Analytics-Engineering-with-dbt

This homework involved **transforming raw NYC Taxi & FHV data** into analytical views using **dbt**. Below are the **final solutions** for each question, along with the necessary SQL code.

---

## **🚀 Completed Tasks & Solutions**  

### **1️⃣ Understanding dbt Model Resolution**  
After setting up `sources.yml` and the environment variables:  
```shell
export DBT_BIGQUERY_PROJECT=myproject
export DBT_BIGQUERY_DATASET=my_nyc_tripdata
```
The following SQL model:  
```sql
select * from {{ source('raw_nyc_tripdata', 'ext_green_taxi' ) }}
```
Compiles to:  
```sql
SELECT * FROM myproject.raw_nyc_tripdata.ext_green_taxi
```
✅ **Correct Answer:** `SELECT * FROM myproject.raw_nyc_tripdata.ext_green_taxi`  

---

### **2️⃣ dbt Variables & Dynamic Models**  
To allow **command-line arguments to override** ENV_VARS and default values, the query was modified to:  
```sql
WHERE pickup_datetime >= CURRENT_DATE - INTERVAL '{{ var("days_back", env_var("DAYS_BACK", "30")) }}' DAY
```
✅ **Correct Answer:**  
✔️ `pickup_datetime >= CURRENT_DATE - INTERVAL '{{ var("days_back", env_var("DAYS_BACK", "30")) }}' DAY'`  

---

### **3️⃣ dbt Data Lineage & Execution**  
Running:  
```shell
dbt run --select models/staging/+ 
```
Would **not** materialize `fct_taxi_monthly_zone_revenue` because `dim_zones.sql` would not have been run.  

✅ **Correct Answer:** `dbt run --select models/staging/+` would **not** materialize `fct_taxi_monthly_zone_revenue`.

---

### **4️⃣ dbt Macros and Jinja**  
Given the macro:  
```sql
{% macro resolve_schema_for(model_type) -%}
    {%- set target_env_var = 'DBT_BIGQUERY_TARGET_DATASET'  -%}
    {%- set stging_env_var = 'DBT_BIGQUERY_STAGING_DATASET' -%}

    {%- if model_type == 'core' -%} {{- env_var(target_env_var) -}}
    {%- else -%}                    {{- env_var(stging_env_var, env_var(target_env_var)) -}}
    {%- endif -%}
{%- endmacro %}
```
✔️ **Correct Answers:**  
✅ `DBT_BIGQUERY_TARGET_DATASET` is **mandatory**, or it fails.  
✅ When using `"core"`, it materializes in `DBT_BIGQUERY_TARGET_DATASET`.  
✅ When using `"staging"`, it defaults to `DBT_BIGQUERY_TARGET_DATASET` if `DBT_BIGQUERY_STAGING_DATASET` is not set.  
✅ `DBT_BIGQUERY_STAGING_DATASET` **is not mandatory**.  

---

### **5️⃣ Taxi Quarterly Revenue Growth Analysis**  
Created **`fct_taxi_trips_quarterly_revenue.sql`** to compute **quarterly revenue** and **YoY Growth**:  
```sql
{{
    config(
        materialized='table'
    )
}}

with temp as (
    SELECT 
        EXTRACT(YEAR FROM pickup_datetime) AS year, 
        EXTRACT(QUARTER FROM pickup_datetime) AS quarter, 
        service_type, 
        total_amount
    FROM {{ ref('fact_trips') }}
),
grouped as (
    SELECT 
        service_type, 
        year, 
        quarter, 
        SUM(total_amount) AS total_amount 
    FROM temp
    GROUP BY service_type, year, quarter
)
SELECT 
    service_type,
    year,
    quarter,
    total_amount,
    LAG(total_amount) OVER (
        PARTITION BY service_type, quarter ORDER BY year
    ) AS prev_year_total_amount,
    CASE 
        WHEN LAG(total_amount) OVER (
            PARTITION BY service_type, quarter ORDER BY year
        ) = 0 THEN NULL  -- Avoid division by zero
        ELSE ROUND(
            (total_amount - LAG(total_amount) OVER (
                PARTITION BY service_type, quarter ORDER BY year
            )) / NULLIF(LAG(total_amount) OVER (
                PARTITION BY service_type, quarter ORDER BY year
            ), 0) * 100, 2
        )
    END AS yoy_percentage_change
FROM grouped
ORDER BY service_type, year, quarter;
```
✅ **Correct Answer:**  
✔️ **Green Taxi:** Best `2020/Q1`, Worst `2020/Q2`  
✔️ **Yellow Taxi:** Best `2020/Q1`, Worst `2020/Q2`  

---

### **6️⃣ P97/P95/P90 Taxi Monthly Fare Analysis**  
Created **`fct_taxi_trips_monthly_fare_p95.sql`** to compute **P97, P95, P90 fares** for April 2020:  
```sql
{{
    config(
        materialized='view'
    )
}}

with temp as (
    SELECT 
        EXTRACT(YEAR FROM pickup_datetime) AS year, 
        EXTRACT(MONTH FROM pickup_datetime) AS month, 
        service_type, 
        fare_amount 
    FROM {{ ref('fact_trips') }}
    WHERE fare_amount > 0 
    AND trip_distance > 0 
    AND payment_type_description IN ('Cash', 'Credit card')
)
SELECT 
    service_type,
    year,
    month,
    PERCENTILE_CONT(fare_amount, 0.90) OVER (PARTITION BY service_type, year, month) AS p90,
    PERCENTILE_CONT(fare_amount, 0.95) OVER (PARTITION BY service_type, year, month) AS p95,
    PERCENTILE_CONT(fare_amount, 0.97) OVER (PARTITION BY service_type, year, month) AS p97
FROM temp 
WHERE year = 2020 AND month = 4
ORDER BY service_type, year, month;
```
✅ **Correct Answer:**  
```json
green: {p97: 55.0, p95: 45.0, p90: 26.5}, 
yellow: {p97: 31.5, p95: 25.5, p90: 19.0}
```  

---

### **7️⃣ Top #Nth Longest P90 Travel Time for FHV**  
Created staging model `stg_fhv_trips.sql`:  
```sql
{{ config(materialized='view') }}

WITH tripdata AS (
  SELECT *,
  FROM {{ source('staging','fhv_tripdata') }}
  WHERE Dispatching_base_num IS NOT NULL 
)
SELECT
    unique_row_id,
    Dispatching_base_num,
    CAST(Pickup_datetime AS TIMESTAMP) AS pickup_datetime,
    CAST(DropOff_datetime AS TIMESTAMP) AS dropoff_datetime,
    {{ dbt.safe_cast("PULocationID", api.Column.translate_type("integer")) }} AS pickup_locationid,
    {{ dbt.safe_cast("DOLocationID", api.Column.translate_type("integer")) }} AS dropoff_locationid,
    SR_Flag
FROM tripdata;
```
✅ **Final Answer (Dropoff Zones for Longest P90 Trips):**  
```json
LaGuardia Airport, Chinatown, Garment District
```  

---

## **🛠 Tools & Technologies Used**  
✅ **dbt Cloud / dbt Core** – Data Transformation  
✅ **BigQuery/Postgres** – Data Warehouse  
✅ **Jinja Macros & dbt Variables** – Dynamic SQL  
✅ **SQL Window Functions & Aggregations** – Analytical Queries  
