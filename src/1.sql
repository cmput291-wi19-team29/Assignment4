-- get the total sum of a certain crime type 
-- within a range of years
-- and separate based on month


SELECT  a1.Month, TotalNum
FROM (SELECT DISTINCT Month FROM crime_incidents WHERE Month BETWEEN 1 and 12) as a1
LEFT JOIN (SELECT Month, SUM(Incidents_Count) AS "TotalNum"
FROM crime_incidents
WHERE Year BETWEEN ? AND ?
AND Crime_Type = ?
GROUP BY Month) AS a2 ON (a1.Month = a2.Month)
ORDER BY a1.Month
