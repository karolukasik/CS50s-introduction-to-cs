SELECT name
FROM people
LEFT JOIN stars ON people.id = stars.person_id
WHERE movie_id = (SELECT id FROM movies WHERE title = "Toy Story");



