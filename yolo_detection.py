import cv2
import os
import uuid
from ultralytics import YOLO

model = YOLO("best.pt")

def process_uploaded_video(video_path):
    # Generate a unique output file name
    output_name = f"{uuid.uuid4().hex}_output.mp4"
    output_path = os.path.join('static/uploads', output_name)

    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0 or fps is None:
        fps = 20.0

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Run YOLO inference
        results = model(frame, verbose=False)
        annotated_frame = results[0].plot() if results else frame

        # Resize annotated frame if necessary
        if (annotated_frame.shape[1], annotated_frame.shape[0]) != (width, height):
            annotated_frame = cv2.resize(annotated_frame, (width, height))

        out.write(annotated_frame)
        frame_count += 1

    cap.release()
    out.release()

    print(f"✅ Processing complete. Total frames: {frame_count}")

    # Return the output file name
    return output_name
