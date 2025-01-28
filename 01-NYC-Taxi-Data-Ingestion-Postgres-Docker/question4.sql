SELECT "lpep_pickup_datetime"::DATE
FROM green_taxi_data
WHERE "trip_distance" = (
        SELECT MAX("trip_distance")
        FROM green_taxi_data
    );