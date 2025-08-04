import cv2
import time
import mediapipe as mp
import numpy as np
from loguru import logger

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)

mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)


def main() -> None:
    video_capture = cv2.VideoCapture(1)
    if not video_capture.isOpened():
        return

    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

    threshold = {
        "x_min": 1000,
        "x_max": -1000,
        "y_min": 1000,
        "y_max": -1000,
        "z_min": 1000,
        "z_max": -1000,
    }

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        start = time.time()

        frame.flags.writeable = False
        results = face_mesh.process(frame)
        frame.flags.writeable = True

        h, w, c = frame.shape

        face_3d = []
        face_2d = []

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                for idx, lm in enumerate(face_landmarks.landmark):
                    if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                        if idx == 1:
                            nose_2d = np.array([lm.x * w, lm.y * h], dtype=np.float64)
                            nose_3d = np.array([lm.x * w, lm.y * h, lm.z * 3000], dtype=np.float64)

                        x, y = int(lm.x * w), int(lm.y * h)

                        # Get 2D coordinates
                        face_2d.append([x, y])

                        # Get 3D coordinates
                        face_3d.append([x, y, lm.z])

                logger.info(f"Face 2D: {face_2d}")
                logger.info(f"Face 3D: {face_3d}")

                # convert to numpy arrays
                face_2d = np.array(face_2d, dtype=np.float64)
                face_3d = np.array(face_3d, dtype=np.float64)

                # The camera matrix
                focal_length = 1 * w
                camera_matrix = np.array([
                    [focal_length, 0, h / 2],
                    [0, focal_length, w / 2],
                    [0, 0, 1]
                ], dtype=np.float64)
                # The distortion matrix
                dist_matrix = np.zeros((4, 1), dtype=np.float64)

                # Solve PnP
                success, rotation_vector, translation_vector = cv2.solvePnP(
                    face_3d,
                    face_2d,
                    camera_matrix,
                    dist_matrix,
                )

                # Get rotational matrix
                rotation_matrix, _ = cv2.Rodrigues(rotation_vector)

                # Get angles
                angles, *extra = cv2.RQDecomp3x3(rotation_matrix)

                # Get the y rotation degree
                x = angles[0] * 360
                y = angles[1] * 360
                z = angles[2] * 360

                threshold["x_min"] = min(threshold["x_min"], x)
                threshold["x_max"] = max(threshold["x_max"], x)
                threshold["y_min"] = min(threshold["y_min"], y)
                threshold["y_max"] = max(threshold["y_max"], y)
                threshold["z_min"] = min(threshold["z_min"], z)
                threshold["z_max"] = max(threshold["z_max"], z)

                if y < -10:
                    message = "Looking Left"
                elif y > 10:
                    message = "Looking Right"
                elif x < -10:
                    message = "Looking Down"
                elif x > 10:
                    message = "Looking Up"
                else:
                    message = "Forward"

                nose_3d_projection, jacobian = cv2.projectPoints(
                    nose_3d,
                    rotation_vector,
                    translation_vector,
                    camera_matrix,
                    dist_matrix
                )

                p1 = (int(nose_2d[0]), int(nose_2d[1]))
                p2 = (int(nose_2d[0] + y * 10), int(nose_2d[1] - x * 10))

                cv2.line(frame, p1, p2, (255, 0, 0), 3)

                cv2.putText(frame, message, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                cv2.putText(frame, f"X: {x:.2f}, Y: {y:.2f}, Z: {z:.2f}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0), 2)

            end = time.time()
            total = end - start
            fps = 1 / total if total > 0 else 0

            cv2.putText(frame, f"FPS: {fps:.2f}", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            # mp_drawing.draw_landmarks(
            #     image=frame,
            #     landmark_list=face_landmarks,
            #     connections=mp_face_mesh.FACEMESH_TESSELATION,
            #     connection_drawing_spec=drawing_spec,
            # )

        cv2.imshow("Face Mesh", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    logger.info(f"X Min: {threshold['x_min']}, X Max: {threshold['x_max']}")
    logger.info(f"Y Min: {threshold['y_min']}, Y Max: {threshold['y_max']}")
    logger.info(f"Z Min: {threshold['z_min']}, Z Max: {threshold['z_max']}")

    video_capture.release()
    cv2.destroyAllWindows()
