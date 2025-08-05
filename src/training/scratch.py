import os
import cv2
import numpy as np
import time
from enum import Enum
from loguru import logger
from typing import List, Optional, Tuple
from insightface.app import FaceAnalysis

THRESHOLD_FACE_CONFIDENCE = 0.5
YAW_THRESHOLD = 25
PITCH_THRESHOLD = 20
ROLL_THRESHOLD = 30


class FaceDirection(Enum):
    FRONTAL = "frontal.png"
    LEFT = "left.png"
    RIGHT = "right.png"
    UPWARD = "upward.png"
    DOWNWARD = "downward.png"


def record_faces():
    video_capture = cv2.VideoCapture(1)
    if not video_capture.isOpened():
        raise RuntimeError("Could not open video device")

    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

    directory = os.path.join(os.getcwd(), "datasets", "faces", "me")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        if cv2.waitKey(1) & 0xFF == ord("s"):
            name = time.time()
            path = os.path.join(directory, f"{name}.png")

            resized_frame = cv2.resize(frame, (640, 640))
            cv2.imwrite(path, resized_frame)
            logger.info(f"Saved frame to {path}")

        cv2.imshow("Face Recording", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video_capture.release()
    cv2.destroyAllWindows()


def exact_image_path(direction: FaceDirection = FaceDirection.FRONTAL) -> str:
    root_directory = os.path.join(os.getcwd(), "datasets", "faces", "me")
    path = os.path.join(root_directory, direction.value)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Image not found at {path}")

    return path


def calculate_pose_angles(landmarks: List[Tuple[float, float]]) -> Tuple[float, float, float]:
    """
    Calculate the pose angles (pitch, yaw, roll) from the facial landmarks.
    Format: landmarks should be a list of (x, y) tuples.
    1. landmarks[0] = left eye
    2. landmarks[1] = right eye
    3. landmarks[2] = nose
    4. landmarks[3] = left mouth corner
    5. landmarks[4] = right mouth corner
    """

    logger.info(f"Landmarks received: {landmarks}")
    # [[291.69278 338.72104]
    # [379.37393 336.56744]
    # [336.9548  386.2869 ]
    # [303.51514 434.7637 ]
    # [370.813   432.61264]]

    # [[891, 974], [736, 852], [803, 1071], [883, 1167], [1033, 856], [962, 1072]]

    return 0, 0, 0


def classify_face_direction(roll: float, pitch: float, yaw: float) -> FaceDirection:
    """
    Classify face direction based on pose angles.

    Args:
        roll: Roll angle in degrees (head tilt left/right)
        pitch: Pitch angle in degrees (head up/down)
        yaw: Yaw angle in degrees (head turn left/right)

    Returns:
        FaceDirection enum indicating the detected direction
    """
    return FaceDirection.FRONTAL


def exact_pose(app: FaceAnalysis, image):
    faces = app.get(image)
    if not faces:
        logger.error("No faces detected in the image.")
        return None

    best_face = max(faces, key=lambda face: face.det_score)
    if best_face.det_score < THRESHOLD_FACE_CONFIDENCE:
        raise ValueError(f"Face confidence score is below the threshold {THRESHOLD_FACE_CONFIDENCE}")

    (roll, pitch, yaw) = calculate_pose_angles(best_face.kps)
    logger.info(f"Detected pose angles: roll={roll}, pitch={pitch}, yaw={yaw}")
    detected_direction = classify_face_direction(roll, pitch, yaw)

    draw_landmarks(image, best_face.kps)
    return detected_direction


def draw_landmarks(image, landmarks):  # Draw landmarks on the image
    # Draw line between two eyes and nose to 2 eyes
    cv2.line(
        image,
        (int(landmarks[0][0]), int(landmarks[0][1])),
        (int(landmarks[1][0]), int(landmarks[1][1])),
        (255, 0, 0),
        2,
    )
    cv2.line(
        image,
        (int(landmarks[0][0]), int(landmarks[0][1])),
        (int(landmarks[2][0]), int(landmarks[2][1])),
        (255, 0, 0),
        2,
    )
    cv2.line(
        image,
        (int(landmarks[1][0]), int(landmarks[1][1])),
        (int(landmarks[2][0]), int(landmarks[2][1])),
        (255, 0, 0),
        2,
    )
    for x, y in landmarks:
        cv2.circle(image, (int(x), int(y)), 2, (0, 255, 0), -1)

    cv2.imshow("Face Landmarks", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def post_estimate(app: FaceAnalysis, face_direction: FaceDirection) -> Optional[FaceDirection]:
    """
    Post-estimation function that is called after the training process.
    5 Case will be handled:
        1. Frontal Face
        2. Left Profile
        3. Right Profile
        4. Upward Facing
        5. Downward Facing
    """
    path = exact_image_path(face_direction)
    image = cv2.imread(path)

    detected_direction = exact_pose(app, image)
    if detected_direction:
        logger.info(f"Expected: {face_direction.name}, Detected: {detected_direction.name}")

        # Check if detection matches expectation
        if detected_direction == face_direction:
            logger.success("✅ Detection matches expected direction!")
        else:
            logger.warning(f"⚠️ Detection mismatch! Expected: {face_direction.name}, Got: {detected_direction.name}")

    return detected_direction


def run_scratch() -> None:
    faces = [
        FaceDirection.FRONTAL,
        FaceDirection.LEFT,
        FaceDirection.RIGHT,
        FaceDirection.UPWARD,
        FaceDirection.DOWNWARD,
    ]

    app = FaceAnalysis(providers=["CPUExecutionProvider"])
    app.prepare(ctx_id=0, det_size=(640, 640))

    # noinspection PyTypeChecker
    for i in range(len(faces)):
        direction = faces[i]
        result = post_estimate(app, direction)
        logger.info(f"Final detected direction: {result.name if result else 'None'}")
