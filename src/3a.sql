-- The main query for Task 3
-- NOTE changing the SELECT results will break the tie-breaking algorithm
SELECT Neighbourhood_Name, SUM(Incidents_Count) AS count
FROM crime_incidents 
WHERE Crime_Type= ?    -- Crime type parameter
AND Year>= ?           -- Start year parameter
AND Year<= ?           -- End year parameter
GROUP BY Neighbourhood_Name 
ORDER BY count DESC;

-- SELECT *
-- FROM crime_incidents 
-- WHERE Crime_Type= "Assault"    -- Crime type parameter
-- AND Year>= ?           -- Start year parameter
-- AND Year<= ?           -- End year parameter
-- GROUP BY Neighbourhood_Name 
-- ORDER BY count DESC;
