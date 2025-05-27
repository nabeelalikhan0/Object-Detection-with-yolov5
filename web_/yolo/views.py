from django.shortcuts import render
from django.http import JsonResponse
from ultralytics import YOLO
from .BlackBox import BlackBoxAI
from collections import Counter
import cv2
import numpy as np
import base64

# Load YOLO model
model = YOLO("yolov5s.pt")

def index(request):
    if request.method == "POST":
        # Get the frame from the request
        frame_data = request.POST.get("frame")
        if frame_data:
            # Decode the base64 image
            frame_bytes = base64.b64decode(frame_data.split(",")[1])
            np_arr = np.frombuffer(frame_bytes, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            # Perform YOLO detection
            results = model.predict(source=frame)
            detected_classes = []

            for result in results:
                for box in result.boxes:
                    cls = int(box.cls[0])  # Class index
                    label = f"{model.names[cls]}"  # Class label
                    detected_classes.append(label)

            # Count occurrences
            class_counts = Counter(detected_classes)
            detection_summary = [f"{count} {label}{'s' if count > 1 else ''}" for label, count in class_counts.items()]
            summary_text = ", ".join(detection_summary) if detection_summary else "No detections"

            # Generate AI response
            ai_response = BlackBoxAI(f"Explain this scene to a blind person: there are {summary_text} in front of you. use as less words as possible")

            user_reply = request.POST.get("input")
            print(user_reply)

            return JsonResponse({"summary": summary_text, "ai_response": ai_response})

    return render(request, "index.html")
