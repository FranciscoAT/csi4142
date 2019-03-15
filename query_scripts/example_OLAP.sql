-- Roll UP Query, gets accidents that occured on an intersection and rolls up based on year > month
SELECT H.month, H.year, count(F.is_intersection) FROM hour H INNER JOIN accidentfact F ON H.hour_key = F.hour_key GROUP BY ROLLUP(H.year, H.month);
-- Roll down query, gets accidents that occured on an intersection and rolls down based on month > year
SELECT H.month, H.year, count(F.is_intersection) FROM hour H INNER JOIN accidentfact F ON H.hour_key = F.hour_key GROUP BY ROLLUP(H.month, H.year);
-- Slice: Gets fatal accidents and groups them by the collision type
SELECT count(F.is_fatal), A.impact_type FROM accidentfact F INNER JOIN accident A ON A.accident_key = F.accident_key WHERE F.is_fatal = 'True' GROUP BY A.impact_type;
-- Dice: gets fatal accidents in kanata and groups them by collision type
SELECT count(F.is_fatal), A.impact_type FROM accidentfact F INNER JOIN accident A ON A.accident_key = F.accident_key INNER JOIN location L ON L.location_key = F.location_key WHERE F.is_fatal = 'True' AND L.neighborhood = 'Kanata' GROUP BY A.impact_type;
-- Iceberg Top N: Fetches top 5 neighborhoods with most accidents
SELECT count(L.neighborhood), L.neighborhood FROM location L INNER JOIN accidentfact F ON F.location_key = L.location_key GROUP BY (L.neighborhood) ORDER BY count(L.neighborhood) DESC FETCH FIRST 5 ROWS ONLY;
-- Iceberg Bottom N: Fetches top 5 neighborhoods with least accidents
SELECT count(L.neighborhood), L.neighborhood FROM location L INNER JOIN accidentfact F ON F.location_key = L.location_key GROUP BY (L.neighborhood) ORDER BY count(L.neighborhood) ASC FETCH FIRST 5 ROWS ONLY;
