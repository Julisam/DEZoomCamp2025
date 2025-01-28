SELECT p."Zone",
    SUM(g."total_amount") AS total_amount
FROM green_taxi_data AS g
    LEFT JOIN taxi_zone_lookup AS p ON g."PULocationID" = p."LocationID"
WHERE g."lpep_pickup_datetime"::DATE = '2019-10-18'
GROUP BY p."Zone"
HAVING SUM(g."total_amount") >= 13000
ORDER BY total_amount DESC;