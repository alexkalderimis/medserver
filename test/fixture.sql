INSERT INTO patient (id, dob, gender) VALUES (1, date '1950-01-02', 'male');
INSERT INTO patient (id, dob, gender) VALUES (2, date '1960-01-03', 'female');
INSERT INTO patient (id, dob, gender) VALUES (3, date '1970-01-04', 'male');
INSERT INTO patient (id, dob, gender) VALUES (4, date '1980-01-05', 'female');

INSERT INTO institution VALUES (1, 'university of x');
INSERT INTO institution VALUES (2, 'university of y');
INSERT INTO institution VALUES (3, 'university of z');

INSERT INTO advisor (id, name, profile, institution) VALUES (1, 'advisor1', 'A good advisor', 1);
INSERT INTO advisor (id, name, profile, institution) VALUES (2, 'advisor2', 'An ok advisor', 2);
INSERT INTO advisor (id, name, profile, institution) VALUES (3, 'advisor3', 'A bad advisor', 3);

INSERT INTO complaint (summary, pain_level, concern_level, patient, area)
       VALUES ('I have a problem with my leg', 5, 3, 1, 1);
INSERT INTO complaint (summary, pain_level, concern_level, patient, area)
       VALUES ('I have a problem with my eye', 6, 8, 2, 2);
INSERT INTO complaint (summary, pain_level, concern_level, patient, area)
       VALUES ('I have a problem with my leg', 5, 3, 3, 3);
INSERT INTO complaint (summary, pain_level, concern_level, patient, area)
       VALUES ('I have a problem with my leg', 1, 5, 4, 4);

INSERT INTO response (advice, complaint, advisor) VALUES ( 'take a pill', 1, 1);
INSERT INTO response (advice, complaint, advisor) VALUES ( 'take some cream', 2, 2);
INSERT INTO response (advice, complaint, advisor) VALUES ( 'see a doctor', 3, 3);


