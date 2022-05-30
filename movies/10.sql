SELECT name
FROM people
    LEFT JOIN directors ON people.id = directors.person_id
    LEFT JOIN ratings ON ratings.movie_id = directors.movie_id
WHERE rating >= 9
GROUP BY people.id;