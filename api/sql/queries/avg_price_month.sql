-- Average price for each coin by month.

SELECT DISTINCT "month", "coin", "avg_price"
FROM(
	SELECT
	b."month" AS "month",
	a.coin AS "coin",
	avg(a.price)OVER(partition by b."month" ORDER BY a.coin) AS "avg_price"
	FROM coin_data a
	INNER JOIN coin_month_data b ON a.coin = b.coin
	ORDER BY "month"
) A;


