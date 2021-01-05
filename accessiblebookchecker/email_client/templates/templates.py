import codecs
import os


def stringify_html(file_path):

    path = os.path.join(os.getcwd(), "templates", file_path)

    with codecs.open(path, 'r') as template:
        email_template = template.read()
        return email_template

def open_file(file_path):

    path = os.path.join(os.getcwd(), "templates", file_path)

    with open(path, 'r') as template:
        text_template = template.read()
        return text_template


def html_email_templates():

    email_templates = {
        'pre_start_email_contact': stringify_html('pre_start_contact_basic.html'),
        'student_activated_accomm': stringify_html('student_requests_captions_early.html'),
        # 'late_add_notification': stringify_html('student_activated_accomm.html'),
        # 'notify_student_of_coverage': stringify_html('notify_student_of_coverage.html')
    }
    return email_templates

def text_email_templates():

    text_templates = {
        # 'pre_start_email_contact': open_file('pre_start_contact_basic.html'),
        'student_activated_accomm': open_file('student_requests_captions_early.txt'),
        # 'late_add_notification': stringify_html('student_activated_accomm.html'),
        # 'notify_student_of_coverage': stringify_html('notify_student_of_coverage.html')

    }
    return text_templates
