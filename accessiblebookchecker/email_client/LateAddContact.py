import smtplib
from email.message import EmailMessage
from captioning.captioning_database.backend_functionality.sf_cap_db_backend_functions.backend_utilities.email_db_functions import get_student_requests_captions
import datetime
import traceback


current_contacts, session = get_student_requests_captions()

 # Session management problem. Can't committ with this architetcuter

print(current_contacts)

message = """ 
Dear {0},

This is a courtesy e-mail from the DPRC Accessible Media Program.

A student enrolled in your course, {1}, recently added a media captioning accommodation through the Disability Programs and Resource Center. 

We want to reach out to you to help make sure any videos used in your course contain closed captions.

Here are a few things to keep in mind. 

•	The DPRC accessible media program can automatically access your iLearn page and start captioning your videos. You do not need to submit video links posted on your iLearn page. We will provide a captioned version to you automatically.

•	If you plan to use physical media (DVDs, VHS) please e-mail captions@sfsu.edu and let us know what you are showing and when you are showing it. 

•	If you are using PowerPoint presentations that contain videos, please let us know so we can start the captioning process.

•	We will automatically activate iLearn lecture capture captions.

If you are using videos on your iLearn page, please keep an eye out for e-mails from captions@sfsu.edu, they may contain captioned versions of videos on your ilearn site. Please add those video links to your course page. 

It can easily take more than a week to get a video captioned. Please submit any requests to us as soon as you know you will need them.

If you have any questions or would like to submit videos to us for captioning, please respond to this e-mail.

If you don’t plan to use any audio/video based instructional materials in your course, there is nothing you need to do at this time.

This is the official captioning service account for the SF State Disability Programs and Resource Center. 

Email: captions@sfsu.edu
Phone: 415-405-2180

"""




for each in current_contacts[0:1]:
    print(each[2].accomm_added_date, each[0].employee_email)

mailserver = smtplib.SMTP('smtp.office365.com', 587)
mailserver.ehlo()
mailserver.starttls()
mailserver.login('captions@sfsu.edu', 'Revertdprc!1')


for contact in current_contacts[0:4]:

    print(contact.Course.course_gen_id, contact.Employee.employee_id)
    msg = EmailMessage()

    course = contact.Course.course_name + "." + contact.Course.course_section
    message_to_send = message.format(contact.Employee.employee_first_name, course)
    print(message_to_send)

    msg.set_content(message_to_send)
    msg['Subject'] = "Video Captioning Requested For {}".format(course)
    msg["FROM"] = "captions@sfsu.edu"
    msg["TO"] = contact.Employee.employee_email


    try:
        mailserver.send_message(msg)


        contact.Course.student_requests_captions_email_sent = True
        contact.Course.student_requests_captions_email_sent = datetime.datetime.utcnow()
        session.commit()
    except:
        print(traceback.print_exc())



mailserver.quit()
session.close()