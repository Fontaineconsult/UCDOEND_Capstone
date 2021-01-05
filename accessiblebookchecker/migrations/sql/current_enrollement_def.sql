
CREATE OR REPLACE VIEW main_1.current_enrollement AS
SELECT studentenrollement.course_reg_number,
       studentenrollement.student_id,
       rawcourselist.id,
       rawcourselist.subject_code,
       rawcourselist.course_number,
       rawcourselist.section_number,
       rawcourselist.class_title,
       rawcourselist.instructor_name,
       rawcourselist.instructor_email,
       rawcourselist.instructor_id,
       rawcourselist.term_code
FROM main_1.studentenrollement
         JOIN main_1.rawcourselist ON studentenrollement.course_reg_number::text = rawcourselist.course_regestration_number::text
WHERE rawcourselist.term_code::text = '{}'::text;