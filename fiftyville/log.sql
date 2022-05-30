-- Keep a log of any SQL queries you execute as you solve the mystery.


-- SELECT id, description
-- FROM crime_scene_reports
-- WHERE year = 2021 AND month = 7 AND day = 28 AND street = 'Humphrey Street';


-- ID of the case is | 295 | Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.


-- SELECT *
-- FROM interviews
-- WHERE year = 2021 AND month = 7 AND day = 28 AND transcript LIKE '%bakery%';

-- Obtained interviews:
-- RUTH | ID 161 | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might  want to look for cars that left the parking lot in that time frame.
-- EUGENE | ID 162 | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.
-- RUTH | ID 163 | As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.


-- SELECT id, hour, minute, license_plate
-- FROM bakery_security_logs
-- WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute <=25 AND minute > 15 AND activity = 'exit';

-- Got the list of nameplates where one of it is thief's nameplate
-- +-----+------+--------+---------------+
-- | id  | hour | minute | license_plate |
-- +-----+------+--------+---------------+
-- | 260 | 10   | 16     | 5P2BI95       |
-- | 261 | 10   | 18     | 94KL13X       |
-- | 262 | 10   | 18     | 6P58WS2       |
-- | 263 | 10   | 19     | 4328GD8       |
-- | 264 | 10   | 20     | G412CB7       |
-- | 265 | 10   | 21     | L93JTIZ       |
-- | 266 | 10   | 23     | 322W7JE       |
-- | 267 | 10   | 23     | 0NTHK55       |
-- +-----+------+--------+---------------+


-- SELECT atm_transactions.account_number, person_id, name, phone_number, passport_number, license_plate
-- FROM atm_transactions
--     LEFT JOIN bank_accounts ON atm_transactions.account_number = bank_accounts.account_number
--     LEFT JOIN people ON bank_accounts.person_id = people.id
-- WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';

-- Obtained the list of people who were withdrawing the money on Legett Street the same day as thief and their passport numbers and license plates:
-- +----------------+-----------+---------+----------------+-----------------+---------------+
-- | account_number | person_id |  name   |  phone_number  | passport_number | license_plate |
-- +----------------+-----------+---------+----------------+-----------------+---------------+
-- | 28500762       | 467400    | Luca    | (389) 555-5198 | 8496433585      | 4328GD8       |
-- | 28296815       | 395717    | Kenny   | (826) 555-1652 | 9878712108      | 30G67EN       |
-- | 76054385       | 449774    | Taylor  | (286) 555-6063 | 1988161715      | 1106N58       |
-- | 49610011       | 686048    | Bruce   | (367) 555-5533 | 5773159633      | 94KL13X       |
-- | 16153065       | 458378    | Brooke  | (122) 555-4581 | 4408372428      | QX4YZN3       |
-- | 25506511       | 396669    | Iman    | (829) 555-5269 | 7049073643      | L93JTIZ       |
-- | 81061156       | 438727    | Benista | (338) 555-6650 | 9586786673      | 8X428L0       |
-- | 26013199       | 514354    | Diana   | (770) 555-1861 | 3592750733      | 322W7JE       |
-- +----------------+-----------+---------+----------------+-----------------+---------------+


-- WITH people_withdrawing_money AS (
--     SELECT name, phone_number, passport_number, license_plate
--     FROM atm_transactions
--         LEFT JOIN bank_accounts ON atm_transactions.account_number = bank_accounts.account_number
--         LEFT JOIN people ON bank_accounts.person_id = people.id
--     WHERE year = 2021
--     AND month = 7
--     AND day = 28
--     AND atm_location = 'Leggett Street'
--     AND transaction_type = 'withdraw'
-- ),
-- cars_lefting_bakerys_parking AS(
--     SELECT license_plate
--     FROM bakery_security_logs
--     WHERE year = 2021
--     AND month = 7
--     AND day = 28
--     AND hour = 10
--     AND minute BETWEEN 15 AND 25
--     AND activity = 'exit'
-- )
-- SELECT name, phone_number, passport_number, people_withdrawing_money.license_plate
-- FROM people_withdrawing_money
--     INNER JOIN cars_lefting_bakerys_parking ON people_withdrawing_money.license_plate = cars_lefting_bakerys_parking.license_plate;

-- Obtained the list of 4 people who were both lefting the parking at given time and were withdrawing money on Leggett Street


-- SELECT *
-- FROM airports
-- WHERE city LIKE "Fiftyville"

-- The abbreviation and ID of Fiftyville's airport


-- SELECT flights.id, hour, minute, city
-- FROM flights
--     LEFT JOIN airports ON flights.destination_airport_id = airports.id
-- WHERE origin_airport_ID = (SELECT id
--                             FROM airports
--                             WHERE city LIKE "Fiftyville")
--     AND day = 29
--     AND month = 7
--     AND year = 2021
-- ORDER BY hour ASC, minute ASC
-- LIMIT 1

--The earliest flight from Fiftyville is to New York City, so this is tle city where thief has escaped
-- +----+------+--------+---------------+
-- | id | hour | minute |     city      |
-- +----+------+--------+---------------+
-- | 36 | 8    | 20     | New York City |
-- +----+------+--------+---------------+

-- WITH people_withdrawing_money AS (
--     SELECT name, phone_number, passport_number, license_plate
--     FROM atm_transactions
--         LEFT JOIN bank_accounts ON atm_transactions.account_number = bank_accounts.account_number
--         LEFT JOIN people ON bank_accounts.person_id = people.id
--     WHERE year = 2021
--     AND month = 7
--     AND day = 28
--     AND atm_location = 'Leggett Street'
--     AND transaction_type = 'withdraw'
-- ),
-- cars_lefting_bakerys_parking AS(
--     SELECT license_plate
--     FROM bakery_security_logs
--     WHERE year = 2021
--     AND month = 7
--     AND day = 28
--     AND hour = 10
--     AND minute BETWEEN 15 AND 25
--     AND activity = 'exit'
-- )
-- SELECT name, phone_number
--     FROM people_withdrawing_money
--     INNER JOIN cars_lefting_bakerys_parking ON people_withdrawing_money.license_plate = cars_lefting_bakerys_parking.license_plate
--     INNER JOIN passengers ON passengers.passport_number = people_withdrawing_money.passport_number
-- WHERE passengers.flight_id = 36;

--The suspects are now limited to two people
-- +-------+----------------+
-- | name  |  phone_number  |
-- +-------+----------------+
-- | Bruce | (367) 555-5533 |
-- | Luca  | (389) 555-5198 |
-- +-------+----------------+


-- SELECT caller, receiver, name
-- FROM phone_calls
--     INNER JOIN people ON phone_calls.receiver = people.phone_number
-- WHERE day = 28
--     AND month = 7
--     AND year = 2021
--     AND duration < 60
--     AND caller IN ('(389) 555-5198','(367) 555-5533')

-- The result is that it was Robin who Was calling Bruce

-- +----------------+----------------+-------+
-- |     caller     |    receiver    | name  |
-- +----------------+----------------+-------+
-- | (367) 555-5533 | (375) 555-8161 | Robin |
-- +----------------+----------------+-------+
