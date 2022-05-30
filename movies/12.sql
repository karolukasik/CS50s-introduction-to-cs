SELECT title
FROM stars
    LEFT JOIN people on people.id = stars.person_id
    LEFT JOIN movies on movies.id = stars.movie_id
WHERE name = "Johnny Depp" OR name = "Helena Bonham Carter"
GROUP BY movie_id
HAVING COUNT(*) > 1;
