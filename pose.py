import cv2
import mediapipe as mp
import smtplib
import ssl
from email.message import EmailMessage
import pygame

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

pygame.mixer.init()


def send_email(image_path):
    sender_email = "mca2438@rajagiri.edu"
    receiver_email = "mca2438@rajagiri.edu"
    password = "kjns hqwx abfu kqmr"

    subject = "⚠️ Suspicious Person Detected"
    body = "A person was detected on camera. See the attached image."

    # Create email
    em = EmailMessage()
    em['From'] = sender_email
    em['To'] = receiver_email
    em['Subject'] = subject
    em.set_content(body)

    with open(image_path, 'rb') as img:
        em.add_attachment(img.read(), maintype='image', subtype='jpeg', filename='intruder.jpg')

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender_email, password)
        smtp.send_message(em)


sent = False

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    if results.pose_landmarks:
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        if not sent:
            img_path = 'intruder.jpg'
            cv2.imwrite(img_path, frame)
            send_email(img_path)
            print("📨 Email sent!")
            pygame.mixer.Sound("beep.mp3").play()
            sent = True

    cv2.imshow('Pose Estimation', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()