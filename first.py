import cv2
from deepface import DeepFace
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)

voices = engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower() or "female" in voice.id.lower():
        engine.setProperty('voice', voice.id)
        break
previous_emotion = None

cap=cv2.VideoCapture(0)
while True:
    key,frame=cap.read()
    results = DeepFace.analyze(frame,actions=['emotion'],enforce_detection=False)
    emotions=results[0]['dominant_emotion']

    if emotions != previous_emotion:
        engine.say(f"You seem {emotions}")
        engine.runAndWait()
        previous_emotion = emotions
    cv2.putText(frame,f'Emotion:{emotions}',(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)

    cv2.imshow("Emotion recognition",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows(1)