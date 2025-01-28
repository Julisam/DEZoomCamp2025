SELECT CASE
        WHEN "trip_distance" <= 1 THEN '1. Up to 1 mile'
        WHEN "trip_distance" <= 3 THEN '2. Between 1-3'
        WHEN "trip_distance" <= 7 THEN '3. Between 3-7'
        WHEN "trip_distance" <= 10 THEN '4. Between 7-10'
        ELSE '5. Over 10'
    END,
    COUNT(*)
FROM green_taxi_data
WHERE "lpep_pickup_datetime" >= '2019-10-01'
    and "lpep_dropoff_datetime" < '2019-11-01'
GROUP BY 1
ORDER BY 1;