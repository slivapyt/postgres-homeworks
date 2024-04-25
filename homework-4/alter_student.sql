-- 1. Создать таблицу student с полями student_id serial, first_name varchar, last_name varchar, birthday date, phone varchar
CREATE TABLE student
(
  student_id serial,
  first_name varchar(50),
  last_name varchar(50),
  birthday date,
  phone varchar
);

SELECT *
FROM student
-- 2. Добавить в таблицу student колонку middle_name varchar
ALTER TABLE student ADD COLUMN middle_name varchar;

SELECT *
FROM student

-- 3. Удалить колонку middle_name

ALTER TABLE student DROP COLUMN middle_name;
SELECT *
FROM student

-- 4. Переименовать колонку birthday в birth_date

ALTER TABLE student RENAME COLUMN birthday TO birth_date;
SELECT *
FROM student

-- 5. Изменить тип данных колонки phone на varchar(32)
ALTER TABLE student ALTER COLUMN phone SET DATA TYPE varchar(32);
SELECT *
FROM student


-- 6. Вставить три любых записи с автогенерацией идентификатора


ALTER TABLE student  ADD PRIMARY KEY(student_id)

INSERT INTO student VALUES (DEFAULT,'Vovan', 'Sas', '23.04.2022', '7893423432');

INSERT INTO student (first_name, last_name, birth_date, phone)
VALUES ('BOBA', 'Sas', '23.04.2022', '7893423432')

SELECT *
FROM student


-- 7. Удалить все данные из таблицы со сбросом идентификатор в исходное состояние
TRUNCATE TABLE student RESTART IDENTITY;