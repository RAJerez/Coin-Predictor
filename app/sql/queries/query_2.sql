SELECT
    coin,
    date
FROM
    (
    SELECT 
        coin,
        date,
        price,
        LAG(price, 1) OVER (PARTITION BY coin ORDER BY date) AS previous_price,
        LAG(price, 2) OVER (PARTITION BY coin ORDER BY date) AS pre_previous_price
    FROM coin_data
    )
WHERE
    price < previous_price AND previous_price < pre_previous_price;









