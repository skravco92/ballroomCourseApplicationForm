import smtplib
from credentials import mailTrapLogin, mailTrapPassword, serviceProviderEmail
from email.mime.text import MIMEText

def send_new_request(customer, email, location, time, comments):
    # SMTP server information
    smtp_server = "smtp.mailtrap.io"
    port = 2525
    login = mailTrapLogin
    password = mailTrapPassword

    # Create the message in HTML format
    context = f"<p> You've got a new request: </p>"
    context += f"<ul>"
    context += f"<li>applicantName: {customer}</li>"
    context += f"<li>emailAddress: {email}</li>"
    context += f"<li>preferLocation: {location}</li>"
    context += f"<li>preferTime: {time}</li>"
    context += f"<li>message: {comments}</li>"
    context += "</ul>"

    # Set sender and receiver information
    sender = email
    receiver = serviceProviderEmail
    msg = MIMEText(context, "html")
    msg["Subject"] = "New Request for Ballroom Dancing Courses"
    msg["from"] = sender
    msg["to"] = receiver

    # Send the email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender, receiver, msg.as_string())
