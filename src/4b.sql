-- given a neighborhood, fetch the most frequent crime type in that area

-- args are: year range [a,b], neighborhood name

SELECT Crime_Type, sum_ FROM
 (
SELECT Neighbourhood_Name, Crime_Type, SUM(Incidents_Count) as sum_
   FROM crime_incidents
  WHERE Year >= ?
    AND Year <= ?
  GROUP BY Neighbourhood_Name, Crime_Type ORDER BY SUM(Incidents_Count) DESC
 )
 WHERE Neighbourhood_Name = ?