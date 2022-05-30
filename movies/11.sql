SELECT title
FROM people
    LEFT JOIN stars ON people.id = stars.person_id
    LEFT JOIN ratings ON ratings.movie_id = stars.movie_id
    LEFT JOIN movies ON movies.id = ratings.movie_id
WHERE name = "Chadwick Boseman"
ORDER BY rating DESC
LIMIT 5;