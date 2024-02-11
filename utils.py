from PIL import Image, ImageTk
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv


def resize_icon(icon_path, width, height):
    # Open the image using PIL
    img = Image.open(icon_path)
    # Resize the image
    resized_img = img.resize((width, height), Image.LANCZOS)
    # Convert the resized image to a PhotoImage object
    resized_icon = ImageTk.PhotoImage(resized_img)
    # Return the resized icon
    return resized_icon


def send_email(subject, body):
    load_dotenv()
    SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
    SENDER_EMAIL_PASSWORD = os.environ.get("SENDER_EMAIL_PASSWORD")

    RECIEVER_EMAIL = os.environ.get("RECIEVER_EMAIL")
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg["subject"] = subject
        msg["to"] = RECIEVER_EMAIL
        msg["from"] = SENDER_EMAIL

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

    except Exception as e:
        print(f"Error sending email: {e}")
