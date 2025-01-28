SELECT d."Zone",
    g."tip_amount"
FROM green_taxi_data AS g
    LEFT JOIN taxi_zone_lookup AS p ON g."PULocationID" = p."LocationID"
    LEFT JOIN taxi_zone_lookup AS d ON g."DOLocationID" = d."LocationID"
WHERE g."lpep_pickup_datetime" between '2019-10-01' and '2019-11-01'
    AND p."Zone" = 'East Harlem North'
ORDER BY g."tip_amount" DESC
LIMIT 1;