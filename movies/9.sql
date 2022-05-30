SELECT name
FROM people
LEFT JOIN stars ON stars.person_id = people.id
LEFT JOIN movies ON movies.id = stars.movie_id
WHERE year = 2004
GROUP BY people.id
ORDER BY birth ASC;