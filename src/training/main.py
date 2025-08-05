import cv2
import asyncio
import time
import os
import numpy as np
import insightface
from loguru import logger
import threading
from queue import Queue
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image


def calculate_pose_angles(landmarks):
    if landmarks is None or len(landmarks) < 5:
        return None, None

    # Sử dụng các điểm landmark chuẩn (5 điểm)
    # landmarks[0] = mắt trái, landmarks[1] = mắt phải, landmarks[2] = mũi
    # landmarks[3] = góc miệng trái, landmarks[4] = góc miệng phải

    left_eye = landmarks[0]
    right_eye = landmarks[1]
    nose = landmarks[2]
    left_mouth = landmarks[3]
    right_mouth = landmarks[4]

    # Tính yaw (góc xoay trái/phải) - sử dụng tỷ lệ khoảng cách mắt
    left_eye_to_nose = abs(left_eye[0] - nose[0])
    right_eye_to_nose = abs(right_eye[0] - nose[0])

    # Tính tỷ lệ để xác định hướng
    total_distance = left_eye_to_nose + right_eye_to_nose
    if total_distance > 0:
        ratio = (right_eye_to_nose - left_eye_to_nose) / total_distance
        yaw = ratio * 60  # Scale to degrees
    else:
        yaw = 0

    # Tính pitch (góc ngẩng/cúi) - sử dụng vị trí tương đối của mũi
    eye_center_y = (left_eye[1] + right_eye[1]) / 2
    mouth_center_y = (left_mouth[1] + right_mouth[1]) / 2
    nose_y = nose[1]

    # Tính vị trí tương đối của mũi giữa mắt và miệng
    if mouth_center_y != eye_center_y:
        nose_ratio = (nose_y - eye_center_y) / (mouth_center_y - eye_center_y)
        # Mũi ở giữa mắt và miệng khi ratio ~ 0.5
        pitch = (nose_ratio - 0.5) * 60  # Scale to degrees
    else:
        pitch = 0

    return yaw, pitch


def classify_pose(yaw, pitch):
    if yaw is None or pitch is None:
        return "unknown"

    if abs(yaw) <= 15 and abs(pitch) <= 15:
        return "front"  # Chính diện
    elif yaw < -15 and abs(pitch) <= 20:
        return "left"  # Nghiêng trái
    elif yaw > 15 and abs(pitch) <= 20:
        return "right"  # Nghiêng phải
    elif abs(yaw) <= 20 and pitch > 10:
        return "up"  # Ngẩng
    elif abs(yaw) <= 20 and pitch < -10:
        return "down"  # Cúi
    else:
        return "other"


face_directory = os.path.join(os.getcwd(), "datasets", "faces", "me")


def record_faces():
    app = FaceAnalysis(providers=["CPUExecutionProvider"])
    app.prepare(ctx_id=0, det_size=(640, 640))

    video_capture = cv2.VideoCapture(1)
    if not video_capture.isOpened():
        raise RuntimeError("Could not open video device")

    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

    frame_queue = Queue(maxsize=10)
    result_queue = Queue(maxsize=5)

    frame_skip = 1  # Detect mọi frame để responsive hơn
    frame_count = 0

    current_pose = "no_face"
    current_yaw = None
    current_pitch = None
    current_landmarks = None

    def detection_worker():
        while True:
            try:
                frame = frame_queue.get(timeout=1.0)
                if frame is None:
                    break

                faces = app.get(cv2.resize(frame, (640, 640)))

                if faces:
                    best_face = max(faces, key=lambda x: x.det_score)
                    if best_face.det_score >= 0.3:
                        while not result_queue.empty():
                            try:
                                result_queue.get_nowait()
                            except:
                                break

                        logger.info(
                            f"Detected face with score: {best_face.det_score:.2f} and landmarks: {best_face.kps}"
                        )
                        # result_queue.put((pose, yaw, pitch, scaled_landmarks))
                    else:
                        if result_queue.empty():
                            result_queue.put(("low_confidence", None, None, None))
                else:
                    if result_queue.empty():
                        result_queue.put(("no_face", None, None, None))

                frame_queue.task_done()
            except:
                break

    detection_threads = []
    for i in range(10):
        thread = threading.Thread(target=detection_worker, daemon=True)
        thread.start()
        detection_threads.append(thread)

    try:
        while True:
            ret, frame = video_capture.read()
            if not ret or frame is None:
                break

            frame_count += 1

            if frame_count % frame_skip == 0:
                while frame_queue.qsize() > 3:
                    try:
                        frame_queue.get_nowait()
                        frame_queue.task_done()
                    except:
                        break

                if not frame_queue.full():
                    frame_queue.put(frame.copy())

            try:
                if not result_queue.empty():
                    current_pose, current_yaw, current_pitch, current_landmarks = result_queue.get_nowait()
            except:
                pass

            if current_landmarks is not None:
                colors = [(0, 255, 255), (255, 0, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
                labels = ["L_Eye", "R_Eye", "Nose", "L_Mouth", "R_Mouth"]

                for i, (point, color, label) in enumerate(zip(current_landmarks, colors, labels)):
                    x, y = int(point[0]), int(point[1])
                    cv2.circle(frame, (x, y), 5, color, -1)
                    cv2.putText(
                        frame,
                        f"{i+1}:{label}",
                        (x + 15, y - 8),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        color,
                        2,
                    )

            info_text = f"Pose: {current_pose}"
            if current_yaw is not None and current_pitch is not None:
                info_text += f" | Yaw: {current_yaw:.1f}° | Pitch: {current_pitch:.1f}°"

            cv2.putText(frame, info_text, (15, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
            cv2.putText(
                frame,
                f"Frame: {frame_count} (Skip: {frame_skip})",
                (15, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
            )

            cv2.putText(
                frame,
                "Press: +/- (skip), q (quit)",
                (15, frame.shape[0] - 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
            )

            cv2.imshow("Video Frame", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            elif key == ord("+") or key == ord("="):
                frame_skip = min(frame_skip + 1, 10)
                print(f"Frame skip: {frame_skip}")
            elif key == ord("-"):
                frame_skip = max(frame_skip - 1, 1)
                print(f"Frame skip: {frame_skip}")

    finally:
        for _ in detection_threads:
            frame_queue.put(None)

        video_capture.release()
        cv2.destroyAllWindows()

        for thread in detection_threads:
            thread.join(timeout=1.0)

        print("Camera stopped")


def main() -> None:
    record_faces()
