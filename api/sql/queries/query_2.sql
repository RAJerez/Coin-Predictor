/*
Calculate for each coin, on average, how much its price has increased after it had
dropped consecutively for more than 3 days. In the same result set include the
current market cap in USD (obtainable from the JSON-typed column). Use any time
span that you find best.
*/



-- get days
SELECT EXTRACT(day FROM 'date') as 'day' FROM 'coin_data'

-- get capitalization in usd
SELECT JSON_VALUE(json, '$.market_data.market_cap.usd') AS usd_cap
FROM 'coin_data';