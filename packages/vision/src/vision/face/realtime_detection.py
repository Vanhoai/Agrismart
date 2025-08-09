import cv2
import queue
import threading
import time
from typing import Optional, List
from loguru import logger
from vision.face import FaceDetector, FaceDetected


class RealtimeDetection:
    def __init__(
        self,
        num_threads: int = 4,
        detect_queue_size: int = 3,
        result_queue_size: int = 5,
        frame_skip: int = 2,
    ) -> None:
        self.num_threads = num_threads
        self.detect_queue_size = detect_queue_size
        self.result_queue_size = result_queue_size
        self.frame_skip = frame_skip

        # initialize
        self.face_detector = FaceDetector()
        self.detect_queue = queue.Queue(self.detect_queue_size)
        self.result_queue = queue.Queue(self.result_queue_size)

        self.tasks: List[threading.Thread] = []
        self.video_capture: Optional[cv2.VideoCapture] = None
        self.running = False
        self.frame_count = 0

        self.latest_detection = None
        self.detection_lock = threading.Lock()

    def detect_worker(self):
        while self.running:
            try:
                frame = self.detect_queue.get(timeout=1.0)
                if frame is None:
                    break

                face_detected = self.face_detector.detect_from_image(frame)

                with self.detection_lock:
                    self.latest_detection = face_detected

                if face_detected and not self.result_queue.full():
                    self.result_queue.put(face_detected)

            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error in detect_worker: {e}")

    def prepare(self):
        self.video_capture = cv2.VideoCapture(1)
        if not self.video_capture.isOpened():
            raise IOError("Couldn't open webcam or video")

        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
        self.video_capture.set(cv2.CAP_PROP_FPS, 30)
        self.video_capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        self.running = True
        for _ in range(self.num_threads):
            task = threading.Thread(target=self.detect_worker, daemon=True)
            task.start()
            self.tasks.append(task)

    def release(self):
        self.running = False

        if self.video_capture:
            self.video_capture.release()
            cv2.destroyAllWindows()

        while not self.detect_queue.empty():
            try:
                self.detect_queue.get_nowait()
            except queue.Empty:
                break

        while not self.result_queue.empty():
            try:
                self.result_queue.get_nowait()
            except queue.Empty:
                break

        for task in self.tasks:
            task.join(timeout=2.0)

        self.tasks.clear()

    def draw_detection(self, frame, face_detected: FaceDetected):
        bbox = face_detected.bbox
        det_score = face_detected.det_score
        keypoints = face_detected.kps

        for x, y in keypoints:
            cv2.circle(frame, (int(x), int(y)), 2, (0, 255, 0), -1)

        cv2.putText(
            frame,
            f"Score: {det_score:.2f}",
            (int(bbox[0]), int(bbox[1]) - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1,
        )

        cv2.rectangle(
            frame,
            (int(bbox[0]), int(bbox[1])),
            (int(bbox[2]), int(bbox[3])),
            (0, 255, 0),
            2,
        )

    def detect(self):
        self.prepare()
        if not self.video_capture:
            logger.error("Video capture is not initialized.")
            return

        prev_time = 0
        next_time = 0

        try:
            while True:
                ret, frame = self.video_capture.read()
                if not ret:
                    logger.warning("Failed to read frame")
                    continue

                self.frame_count += 1
                if self.frame_count % (self.frame_skip + 1) != 0:
                    with self.detection_lock:
                        if self.latest_detection:
                            self.draw_detection(frame, self.latest_detection)
                else:
                    if not self.detect_queue.full():
                        while not self.detect_queue.empty():
                            try:
                                self.detect_queue.get_nowait()
                            except queue.Empty:
                                break

                        self.detect_queue.put(frame.copy())

                    try:
                        face_detected = self.result_queue.get_nowait()
                        if face_detected:
                            self.draw_detection(frame, face_detected)
                    except queue.Empty:
                        with self.detection_lock:
                            if self.latest_detection:
                                self.draw_detection(frame, self.latest_detection)

                next_time = time.time()
                fps = 1 / (next_time - prev_time) if prev_time else 0
                prev_time = next_time

                cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                cv2.imshow("Webcam Feed", frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
                elif key == ord("r"):
                    with self.detection_lock:
                        self.latest_detection = None

        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        except Exception as e:
            logger.error(f"Error in detection loop: {e}")
        finally:
            self.release()
