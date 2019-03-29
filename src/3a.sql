-- The main query for Task 3
SELECT Neighbourhood_Name, COUNT(*) AS count 
FROM crime_incidents 
WHERE Crime_Type= ?    -- Crime type parameter
AND Year>= ?           -- Start year parameter
AND Year<= ?           -- End year parameter
GROUP BY Neighbourhood_Name 
ORDER BY count DESC;

-- sample query:
-- SELECT Crime_Type, Neighbourhood_Name, COUNT(*) AS count 
-- FROM crime_incidents 
-- WHERE Crime_Type="Assault" AND Year=2012 
-- GROUP BY Neighbourhood_Name 
-- ORDER BY count DESC;