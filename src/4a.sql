-- Given a range of years and an integer N, show (in a map) the Top-N neighborhoods with the highest crimes to 
-- population ratio within the provided range. Also, show the most frequent crime type in each of these neighborhoods.

-- do not consider the neighbourhoods which do not have a reported population

-- args are in the format [a, b], n

  SELECT reviewer 
    FROM reviews 
GROUP BY reviewer 
  HAVING COUNT(*) >= ? 
     AND COUNT(*) <= ?;

