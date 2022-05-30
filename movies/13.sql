WITH kevin_bacons_movies_ids AS (
    SELECT movie_id
    FROM stars
    WHERE person_id = (
        SELECT id
        FROM people
        WHERE name = "Kevin Bacon" AND birth = 1958)
)
SELECT name
FROM people
    INNER JOIN stars ON stars.person_id = people.id
    INNER JOIN kevin_bacons_movies_ids ON stars.movie_id = kevin_bacons_movies_ids.movie_id
WHERE name != "Kevin Bacon"
GROUP BY people.id;





