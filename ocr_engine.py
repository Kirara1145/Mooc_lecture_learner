import numpy as np
from rapidocr import EngineType, RapidOCR


class OcrEngine:
    def __init__(self) -> None:
        self._engine = RapidOCR(
            params={
                "Det.engine_type": EngineType.OPENVINO,
                "Cls.engine_type": EngineType.OPENVINO,
                "Rec.engine_type": EngineType.OPENVINO,
            }
        )

    def recognize(self, img: np.ndarray):
        result = self._engine(img)
        boxes = result.boxes
        if boxes is None:
            boxes = np.empty((0, 4, 2), dtype=np.float32)
        return {
            "txts": result.txts or (),
            "boxes": boxes,
            "scores": result.scores or (),
        }


_engine = None


def get_engine() -> OcrEngine:
    global _engine
    if _engine is None:
        _engine = OcrEngine()
    return _engine


def recognize(img: np.ndarray):
    return get_engine().recognize(img)


def recognize_roi(img: np.ndarray, roi):
    import screen

    crop = screen.crop_roi(img, roi)
    ox, oy = screen.roi_origin(roi)
    result = recognize(crop)
    boxes = result["boxes"].copy()
    if len(boxes):
        boxes[:, :, 0] += ox
        boxes[:, :, 1] += oy
    result["boxes"] = boxes
    return result
