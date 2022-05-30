WITH helenas_movies_ids AS(
    SELECT movie_id
    FROM stars
    WHERE person_id = (
        SELECT id
        FROM people
        WHERE name = "Helena Bonham Carter"
    )
),
johnnys_movies_ids AS(
    SELECT movie_id
    FROM stars
    WHERE person_id = (
        SELECT id
        FROM people
        WHERE name = "Johnny Depp"
    )
)
SELECT title
FROM movies
    INNER JOIN helenas_movies_ids ON helenas_movies_ids.movie_id = movies.id
    INNER JOIN johnnys_movies_ids ON johnnys_movies_ids.movie_id = movies.id;

-- SELECT title
-- FROM stars
--     LEFT JOIN people on people.id = stars.person_id
--     LEFT JOIN movies on movies.id = stars.movie_id
-- WHERE name = "Johnny Depp" OR name = "Helena Bonham Carter"
-- GROUP BY movie_id
-- HAVING COUNT(*) > 1;
