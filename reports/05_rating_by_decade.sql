-- 05_rating_by_decade.sql
-- Description: Analyzes user's rating patterns across different decades.
-- This can reveal if the user has a preference for movies from a certain era.
-- Groups movies by decade and calculates the average rating and number of movies rated.
-- Replace `?` with the desired user_id.

SELECT
    (FLOOR(EXTRACT(YEAR FROM m.release_date) / 10) * 10) AS decade,
    COUNT(m.id) AS movies_rated,
    ROUND(AVG(umr.rating), 2) AS average_rating
FROM
    user_movie_ratings umr
JOIN
    movies m ON umr.movie_id = m.id
WHERE
    umr.user_id = 1 -- Placeholder for user_id
    AND m.release_date IS NOT NULL
GROUP BY
    decade
ORDER BY
    decade DESC;
