-- 01_top_rated_genres.sql
-- Description: Finds the top-rated movie genres for a specific user based on their average rating.
-- Filters for genres where the user has rated at least 2 movies to provide more meaningful results.
-- Replace `?` with the desired user_id.

SELECT
    g.name AS genre,
    COUNT(m.id) AS movies_rated,
    ROUND(AVG(umr.rating), 2) AS average_rating
FROM
    user_movie_ratings umr
JOIN
    movies m ON umr.movie_id = m.id
JOIN
    movie_genre_association mga ON m.id = mga.movie_id
JOIN
    genres g ON mga.genre_id = g.id
WHERE
    umr.user_id = 1 -- Placeholder for user_id
GROUP BY
    g.name
HAVING
    COUNT(m.id) >= 2
ORDER BY
    average_rating DESC,
    movies_rated DESC;
