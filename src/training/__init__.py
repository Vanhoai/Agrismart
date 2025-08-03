import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image


def main() -> None:
    path = "/Users/hinsun/Workspace/Software/Agrismart/datasets/faces/me/face_1754202317.jpg"
    image = cv2.imread(path)
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # convert image to numpy array
    image = np.array(image)

    app = FaceAnalysis(providers=["CPUExecutionProvider"])
    app.prepare(ctx_id=0, det_size=(640, 640))
    faces = app.get(image)
    results = []

    for face in faces:
        if face.det_score > 0.5:  # filter out low confidence detections
            result = {
                "bbox": face.bbox.astype(int),
                "embedding": face.embedding,
                "confidence": face.det_score,
                "landmarks": face.kps,
                "age": getattr(face, "age", None),
                "gender": getattr(face, "gender", None),
            }
            results.append(result)

    print(f"Detected {len(results)} faces.")
    for i, res in enumerate(results):
        print(f"Face {i + 1}:")
        print(f"  Bounding Box: {res['bbox']}")
        print(f"  Embedding: {res['embedding'][:5]}...")  # Print first 5 dimensions of embedding
        print(f"  Confidence: {res['confidence']:.2f}")
        print(f"  Landmarks: {res['landmarks']}")
        if res["age"] is not None:
            print(f"  Age: {res['age']}")
        if res["gender"] is not None:
            print(f"  Gender: {res['gender']}")

    # Show the first detected face with bounding box
    if results:
        face = results[0]
        bbox = face["bbox"]
        cv2.rectangle(image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
        cv2.putText(
            image,
            f"Age: {face['age']}, Gender: {face['gender']}",
            (bbox[0], bbox[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2,
        )
        cv2.imshow("Detected Face", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
