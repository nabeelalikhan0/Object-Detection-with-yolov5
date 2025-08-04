from django.shortcuts import render
from django.http import JsonResponse
from ultralytics import YOLO
# from .BlackBox import BlackBoxAI
from .Gemini import Gemini
from collections import Counter
import cv2
import numpy as np
import base64

# Load YOLO model once
model = YOLO("yolo11n.pt")
# model = YOLO("yolov5s.pt")

def index(request):
    ai_response = ""

    if request.method == "POST":
        user_reply = request.POST.get("input", "").strip()
        frame_data = request.POST.get("frame")

        # 🧠 Handle text or voice input
        if user_reply:
            print(f"[User Input] {user_reply}")
            ai_response = f"AI Response: {Gemini(user_reply)}"
            print(ai_response)
            return render(request, "index.html", {"ai_response": ai_response})

        # 📸 Handle camera object detection
        if frame_data:
            try:
                frame_bytes = base64.b64decode(frame_data.split(",")[1])
                np_arr = np.frombuffer(frame_bytes, np.uint8)
                frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                results = model.predict(source=frame)
                detected_classes = []

                for result in results:
                    for box in result.boxes:
                        cls = int(box.cls[0])
                        label = model.names[cls]
                        detected_classes.append(label)

                class_counts = Counter(detected_classes)
                detection_summary = [
                    f"{count} {label}{'s' if count > 1 else ''}"
                    for label, count in class_counts.items()
                ]
                summary_text = ", ".join(detection_summary) if detection_summary else "No detections"

                # Prompt for scene explanation
                prompt = f"Explain this scene to a blind person: there are {summary_text} in front of you. Use as few words as possible."
                ai_response = f"AI Response: {Gemini(prompt)}"
                print(ai_response)

                return JsonResponse({"summary": summary_text, "ai_response": ai_response})

            except Exception as e:
                return JsonResponse({"error": str(e)})

    return render(request, "index.html", {"ai_response": ai_response})
