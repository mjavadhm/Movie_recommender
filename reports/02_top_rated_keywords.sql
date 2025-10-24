-- 02_top_rated_keywords.sql
-- Description: Finds the top-rated movie keywords for a specific user.
-- This helps identify specific themes and topics the user enjoys.
-- Filters for keywords present in at least 2 movies rated by the user.
-- Replace `?` with the desired user_id.

SELECT
    k.name AS keyword,
    COUNT(m.id) AS movies_rated,
    ROUND(AVG(umr.rating), 2) AS average_rating
FROM
    user_movie_ratings umr
JOIN
    movies m ON umr.movie_id = m.id
JOIN
    movie_keyword_association mka ON m.id = mka.movie_id
JOIN
    keywords k ON mka.keyword_id = k.id
WHERE
    umr.user_id = 1 -- Placeholder for user_id
GROUP BY
    k.name
HAVING
    COUNT(m.id) >= 2
ORDER BY
    average_rating DESC,
    movies_rated DESC
LIMIT 20; -- Limit to top 20 for brevity
