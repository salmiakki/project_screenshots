import os
import cv2

from screenqual.models.banner_classification.neural_network import model_classify
from screenqual.core.analyser_result import AnalyserResult
from screenqual.filter.screenshot_analyser import ScreenshotAnalyser


class BannerAnalyser(ScreenshotAnalyser):
    def __init__(self):
        super(ScreenshotAnalyser, self).__init__()
        path_to_model = os.path.join(os.path.dirname(__file__),
                                     "../models/banner_classification/weights_sign1.hdf5")
        self.__model = model_classify()
        self.__model.load_weights(path_to_model)

    def execute(self, screenshot):
        h, w, _ = screenshot.image.shape
        img = screenshot.image
        if w > h:
            w //= 3
        else:
            h = w // 3

        img = cv2.resize(img[:h, -w:], (100, 100)).reshape((1, 100, 100, 3)) / 255
        banner_probability = self.__model.predict(img)[0]
        is_banner = banner_probability.argmax(axis=0)
        if is_banner:
            return AnalyserResult.with_anomaly() #{"probability": banner_probability[1]})
        return AnalyserResult.without_anomaly() #{"probability": banner_probability[0]})