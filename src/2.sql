-- Get the total population of each neighbourhood
-- (obtained by summing the three categories of census response)

SELECT c.Neighbourhood_Name, c.Latitude, c.Longitude, p.total
FROM coordinates c, (
    SELECT Neighbourhood_Name, (sum(CANADIAN_CITIZEN)+sum(NON_CANADIAN_CITIZEN)+sum(NO_RESPONSE)) AS total 
    FROM population 
    GROUP BY Neighbourhood_Name
) p
WHERE c.Neighbourhood_Name=p.Neighbourhood_Name
AND c.Latitude!=0.0 AND c.Longitude!=0.0 and p.total!=0 -- Ignore the "zero" entries
ORDER BY p.total DESC;