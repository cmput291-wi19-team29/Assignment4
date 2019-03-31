-- Given a range of years and an integer N, show (in a map) the Top-N neighborhoods with the highest crimes to 
-- population ratio within the provided range. Also, show the most frequent crime type in each of these neighborhoods.

-- args are in the format year range [a, b]
-- filter by empty population / zero longitude-latitude, ratio (descending)

SELECT pop.Neighbourhood_Name, 
       pop.lat,
       pop.long,
       (CAST(crime.total AS FLOAT) / CAST(pop.total AS FLOAT)) as ratio
  FROM 
        (
         SELECT c.Neighbourhood_Name, c.Latitude as lat, c.Longitude as long, p.total AS total
           FROM coordinates c, (
                                SELECT Neighbourhood_Name, 
                                        ( sum(CANADIAN_CITIZEN) + sum(NON_CANADIAN_CITIZEN) + sum(NO_RESPONSE) ) AS total 
                                        FROM population 
                                        GROUP BY Neighbourhood_Name
                              ) p
          WHERE c.Neighbourhood_Name = p.Neighbourhood_Name
            AND c.Latitude != 0.0 AND c.Longitude != 0.0 and p.total != 0
        ) pop,
        (
          SELECT Neighbourhood_Name, 
                 SUM(Incidents_Count) AS total
            FROM crime_incidents 
           WHERE Year >= ?
             AND Year <= ?
        GROUP BY Neighbourhood_Name
        ) crime
 WHERE pop.Neighbourhood_Name == crime.Neighbourhood_Name
 ORDER BY ratio DESC;