CREATE OR REPLACE VIEW main_1.current_student_courses AS
SELECT student.student_id,
       student.student_first_name,
       student.student_last_name,
       student.student_email,
       student.student_requests,
       student.captioning_active,
       student.transcripts_only,
       current_enrollement.course_reg_number,
       current_enrollement.subject_code,
       current_enrollement.course_number,
       current_enrollement.section_number,
       current_enrollement.class_title,
       current_enrollement.instructor_id,
       current_enrollement.instructor_name,
       current_enrollement.instructor_email,
       (('{}'::text || replace(current_enrollement.subject_code::text, ' '::text, ''::text)) || replace(current_enrollement.course_number::text, ' '::text, ''::text)) || current_enrollement.section_number::text AS course_gen_key
FROM main_1.student
         JOIN main_1.current_enrollement ON btrim(student.student_id::text) = btrim(current_enrollement.student_id::text);