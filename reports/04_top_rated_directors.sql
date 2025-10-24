-- 04_top_rated_directors.sql
-- Description: Finds the top-rated directors for a specific user.
-- This helps understand whose directorial style the user prefers.
-- Filters for directors who have directed at least 2 movies rated by the user.
-- Replace `?` with the desired user_id.

SELECT
    p.name AS director,
    COUNT(m.id) AS movies_rated,
    ROUND(AVG(umr.rating), 2) AS average_rating
FROM
    user_movie_ratings umr
JOIN
    movies m ON umr.movie_id = m.id
JOIN
    movie_crew_association mca ON m.id = mca.movie_id
JOIN
    persons p ON mca.person_id = p.id
WHERE
    umr.user_id = 1 -- Placeholder for user_id
    AND mca.job = 'Director'
GROUP BY
    p.name
HAVING
    COUNT(m.id) >= 2
ORDER BY
    average_rating DESC,
    movies_rated DESC
LIMIT 20;
