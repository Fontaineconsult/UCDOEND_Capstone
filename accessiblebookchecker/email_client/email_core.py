import captioning.captioning_database.backend_functionality.sf_cap_db_backend_functions.backend_utilities.email_db_functions as Groups
import smtplib
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import make_msgid
from abc import ABC, abstractmethod
from email_client.templates.templates import html_email_templates, text_email_templates
import os, datetime, time

myDPRC_image = 'img\\myDPRC.png'
cc_image = 'img\\cc.png'
html_templates = html_email_templates()
text_templates = text_email_templates()


def format_semester(string):
    semester_format = {

        'sp20': 'Spring 2020',
        'su20': 'Summer 2020',
        'fa20': 'Fall 2020',
        'sp21': 'Spring 2021',
        'su21': 'Summer 2021',
        'fa21': 'Fall 2021',
        'sp22': 'Spring 2022',
        'su22': 'Summer 2022',
        'fa22': 'Fall 2022'

    }

    return semester_format[string]


class EmailMessage:

    def __init__(self, sender, receiver, subject, text_template, html_template, template_variables):
        self.receiver = receiver
        self.sender = sender
        self.subject = subject
        self.message = MIMEMultipart('alternative')
        self.images = {}
        self.text_template = text_template
        self.html_template = html_template
        self.template_variables = template_variables
        self.make_images()
        self.generate_template()



    def make_images(self):

        for image in self.template_variables['images']:
            file = os.path.join(os.getcwd(), "img", image)
            msg_id = make_msgid(domain='captions@sfsu.edu')

            with open(file, 'rb') as img:
                mime_image = MIMEImage(img.read(), name=file)
                mime_image.add_header('Content-Disposition', 'attachment', filename=image)
                mime_image.add_header('X-Attachment-Id', msg_id)
                mime_image.add_header('Content-ID', msg_id)
                self.images[image] = mime_image
            self.message.attach(self.images[image])


    def generate_template(self):


        course_name = self.template_variables['course_id'] + "." + self.template_variables['course_section']

        # Attach text template
        self.text_template = self.text_template.format(self.template_variables['first_name'],
                                                       course_name,
                                                       self.template_variables['semester'])
        text_message = MIMEText(self.text_template, 'plain')
        self.message.attach(text_message)

        # Attach html template
        self.html_template = self.html_template.format(self.template_variables['first_name'],
                                                       course_name,
                                                       self.template_variables['semester'],
                                             self.images['cc_45.png']['Content-ID'][1:-1], # fix, use variable
                                            # self.images['myDPRC.png']['Content-ID'][1:-1] # removed signature
                                                       )
        html_message = MIMEText(self.html_template, 'html')
        self.message.attach(html_message)



        self.message.add_header("Importance", "high")

        self.message['Subject'] = self.subject.format(course_name, self.template_variables['semester'])
        self.message['From'] = self.sender
        self.message['To'] = self.receiver

    def return_email(self):
        return self.message

    def __repr__(self):
        return "< e-mail object for {} for {} >".format(self.receiver,
                                                        self.template_variables['course_id']
                                                        + "." + self.template_variables['course_section'])

class SendEmails(ABC):

    def __init__(self):
        self.db_session = None
        self.contacts = None
        self.queried_tables = None
        self.html_email_template = None
        self.text_email_template = None
        self.database_flag = None
        self.flag_table = None
        self.subject = None
        self.images = []
        self.emails = {}
        self.sender = 'captions@sfsu.edu'
        self.email_server = smtplib.SMTP('smtp.office365.com', 587)
        self.assign_contacts()


    @abstractmethod
    def assign_contacts(self):
        pass

    def open_connection(self):
        self.email_server.ehlo()
        self.email_server.starttls()
        self.email_server.login('captions@sfsu.edu', 'Revertdprc!1')


    def generate_emails(self):

        self.contacts = self.db_session.query_response

        for contact in self.contacts:

            person, course = contact[0], contact[1]

            template_variables = {
                "first_name": person.employee_first_name,
                "semester": format_semester(course.semester),
                "course_id": course.course_name,
                "course_section": course.course_section,
                "images": self.images
            }

            reciever_email = contact.Employee.employee_email
            # reciever_email = "fontaine@sfsu.edu"

            self.emails[person.employee_email] = EmailMessage(self.sender,
                                                              reciever_email,
                                                              self.subject,
                                                              self.text_email_template,
                                                              self.html_email_template,
                                                              template_variables)

    def send_all_emails(self):

        self.open_connection()

        for contact in self.contacts:
            time.sleep(4)
            try:
                # Add print feedback
                self.email_server.send_message(self.emails[contact.Employee.employee_email].return_email())
                flag_table = getattr(contact, self.flag_table)
                setattr(flag_table, self.database_flag, True)
                setattr(flag_table, self.database_flag + "_date", datetime.datetime.utcnow())
                print("Sent E-mail for ", contact)
            except:
                print(traceback.print_exc())
                break


        self.db_session.commit()
        self.email_server.close()


    def send_email_to(self, key):
        self.open_connection()
        self.email_server.send_message(self.emails[key].message)
        self.email_server.close()


class NotifyInstructorsStudentsEnrolled(SendEmails):

    """
    contact_email_sent

    """
    def assign_contacts(self):
        self.queried_tables = ['Employee', 'Course']
        self.db_session = Groups.UncontactedCurrentInstructors(self.queried_tables)
        self.html_email_template = html_templates['pre_start_email_contact']
        self.subject = "Video captioning eligibility for {0}"
        self.database_flag = 'contact_email_sent'
        self.flag_table = 'Course'
        self.images = ['cc_45.png']




class NotifyInstructorsStudentsWantCaptions(SendEmails):

    """
    student_requests_captions_email_sent

    """
    def assign_contacts(self):
        self.queried_tables = ['Employee', 'Course', 'Enrollment']
        self.db_session = Groups.StudentsRequestingCaptioning(self.queried_tables)
        self.html_email_template = html_templates['student_activated_accomm']
        self.text_email_template = text_templates['student_activated_accomm']
        self.subject = "Video Captioning Requested for {0} - {1}"
        self.database_flag = 'student_requests_captions_email_sent'
        self.flag_table = 'Course'
        self.images = ['cc_45.png',
                       ]





class NotifyStudentsReceivingCaptioning(SendEmails):

    def __init__(self):
        pass


emails = NotifyInstructorsStudentsWantCaptions()
emails.generate_emails()
# emails.send_email_to('jolie@sfsu.edu')
print(emails.emails)
emails.send_all_emails()
