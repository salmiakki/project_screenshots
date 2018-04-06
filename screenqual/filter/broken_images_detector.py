import numpy as np
import cv2
from screenqual.filter.screenshot_analyser import ScreenshotAnalyser
from screenqual.core.analyser_result import AnalyserResult


class BrokenImagesAnalyser(ScreenshotAnalyser):
    def execute(self, screenshot):
        img = screenshot.image
        # Image pre-processing
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
        kernel = np.ones((20, 20), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        f, contours, h = cv2.findContours(thresh, 1, 2)
        w, h, _ = img.shape
        min_area = w * h * 0.002
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            if len(approx) == 4:
                area = cv2.contourArea(approx)
                if (area >= min_area):
                    y_vals = approx[:, 0, 1]
                    x_vals = approx[:, 0, 0]
                    x_vals.sort()
                    y_vals.sort()
                    # Chose the left downside corner of the rectangular as base colour
                    # for comparision
                    base_colour = img[y_vals[1] + 5][x_vals[1] + 5]
                    rect = img[y_vals[1] + 5:y_vals[2] - 5, x_vals[1] + 5:x_vals[2] - 5]
                    colour_arr = np.full(rect.shape, base_colour)
                    if np.all(rect == colour_arr):
                        return AnalyserResult.with_anomaly()
        return AnalyserResult.without_anomaly()

