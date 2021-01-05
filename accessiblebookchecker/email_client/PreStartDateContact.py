import smtplib
from email.message import EmailMessage
from captioning.captioning_database.backend_functionality.sf_cap_db_backend_functions.backend_utilities.email_db_functions import get_current_instructors_contact




current_contacts = get_current_instructors_contact()



print(current_contacts)

message = """ 
Dear {0},

This is a courtesy e-mail from the DPRC Accessible Media Program.

In order to help you prepare your instructional materials for the Fall 2019 semester, we would like to inform you that a DPRC student with deaf or hard of hearing disability is enrolled in your course, {1}. This student is eligible to receive a media closed captioning accommodation for any audio/video based instructional materials used in this course.

While this student is eligible for a media captioning accommodation through the DPRC, at this point in time they may or may not have elected to use this accommodation for {1}. They can, however, elect to use this accommodation at any time during the semester.

In order to avoid complications and extra work placed on you due to last minute changes in this student’s accommodation, we want to inform you now so we can work with you to prepare any captioning required for your instructional materials.

•	If you primarily use iLearn to host your instructional videos, please activate your iLearn page as soon as you can. The DPRC accessible media program can automatically access your iLearn page and start captioning your videos. You do not need to submit video links posted on your iLearn page. We will provide a captioned version to you automatically.

•	If you plan to use physical media (DVDs, VHS) within the first three weeks of the semester, please inform us now and we will start the captioning process immediately. 

•	If you are using PowerPoint presentations that contain videos, please let us know so we can start the captioning process.

•	We will automatically activate iLearn lecture capture captions.

Just to be clear, this e-mail is to inform you that this student is eligible for a media captioning accommodation, but may not have yet specifically requested the use of that accommodation for this course.

If this student chooses to use their media captioning accommodation for {1} you will receive an official accommodation notification letter from the DPRC. The accessible media program will contact you again to iron out any details.

If you have any questions or would like to submit videos to us for captioning, please respond to this e-mail.

If you don’t plan to use any audio/video based instructional materials in your course, there is nothing you need to do at this time.

This is the official captioning service account for the DPRC. 

Email: captions@sfsu.edu
Phone: 415-405-2180

"""

mailserver = smtplib.SMTP('smtp.office365.com', 587)
mailserver.ehlo()
mailserver.starttls()
mailserver.login('captions@sfsu.edu', 'Revertdprc!1')


for contact in current_contacts:

    print(contact.Course.course_gen_id, contact.Employee.employee_id)
    msg = EmailMessage()

    course = contact.Course.course_name + "." + contact.Course.course_section
    message_to_send = message.format(contact.Employee.employee_first_name, course)
    print(message_to_send)

    msg.set_content(message_to_send)
    msg['Subject'] = "Video Captioning Eligibility For {}".format(course)
    msg["FROM"] = "captions@sfsu.edu"
    msg["TO"] = contact.Employee.employee_email
    mailserver.send_message(msg)


    contact.Course.contact_email_sent = True

mailserver.quit()


# for contact in current_contacts:
#     msg = EmailMessage()
#
#
#     course = contact[2] + "." + contact[3]
#
#     message_to_send = message.format(contact[0], course)
#     email = contact[1]
#     print(email, course)
#
#     msg.set_content(message_to_send)
#     msg['Subject'] = "Video Captioning Eligibility For {}".format(course)
#     msg["FROM"] = "captions@sfsu.edu"
#     msg["TO"] = email
#
#
#     mailserver.send_message(msg)
#
#
# mailserver.quit()
#
#
