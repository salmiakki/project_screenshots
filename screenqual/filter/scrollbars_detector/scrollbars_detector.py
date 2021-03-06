import numpy as np
import cv2
from screenqual.filter.screenshot_analyser import ScreenshotAnalyser
from screenqual.core.analyser_result import AnalyserResult


# Extract only vertical lines that may be vertical scrollbars
def vertical_lines(lines, height, width):
    vertical = []
    for line in lines:
        for x1,y1,x2,y2 in line:
            if abs(y2 - y1) >= height / 6 and x1 == x2 and x1 >= width * 0.90:
                vertical.append((x1, y1, x2, y2))
    return vertical


# Extract only horizontal lines that may be horizontal scrollbars
def horizontal_lines(lines, height, width):
    horizontal = []
    for line in lines:
        for x1,y1,x2,y2 in line:
            if abs(x2 - x1) >= width / 2 and y1 == y2 and y1 >= height * 0.90:
                # note the order of the appended elements
                horizontal.append((y1, x1, y2, x2))
    return horizontal


def check_if_vertical(lines, height, width, img):
    lines = vertical_lines(lines, height, width)
    if (len(lines) < 2):
        return False
    lines.sort() # Should sort based on x1 first
    lines.reverse()
    fx1, fy1, fx2, fy2 = lines[0]
    for idx in range(len(lines)):
        sx1, sy1, sx2, sy2 = lines[idx]
        if fx1 - sx1 > 3:  # thresholds many lines on the same space
            if fx1 - sx1 < width * 0.1:
                return True
            else:
                fx1, fy1, fx2, fy2 = sx1, sy1, sx2, sy2
    return False


def check_if_horizontal(lines, height, width, img):
    lines = horizontal_lines(lines, height, width)
    if len(lines) < 2:
        return False
    lines.sort()  # Should sort based on y1 first
    lines.reverse()
    fy1, fx1, fy2, fx2 = lines[0]
    for idx in range(len(lines)):
        sy1, sx1, sy2, sx2 = lines[idx]
        if fy1 - sy1 > 3:  # threshholding many lines on the same space
            if fy1 - sy1 < height * 0.1:
                return True
            else:
                fy1, fx1, fy2, fx2 = sy1, sx1, sy2, sx2
    return False


class ScrollBarAnalyser(ScreenshotAnalyser):
    def execute(self, screenshot):
        img = screenshot.image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 200, apertureSize=3)
        minLineLength = 200
        maxLineGap = 40
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength, maxLineGap)
        # No lines were detected
        if lines is None:
            return AnalyserResult.without_anomaly({"warning": "Couldn't detect lines"})
        height, width = edges.shape

        has_horizontal_scrollbars = check_if_horizontal(lines, height, width, img)
        has_vertical_scrollbars = check_if_vertical(lines, height, width, img)

        if not has_horizontal_scrollbars and not has_vertical_scrollbars:
            return AnalyserResult.without_anomaly()
        elif has_horizontal_scrollbars and not has_vertical_scrollbars:
            return AnalyserResult.with_anomaly({"cause": "Horizontal scrollbars detected"})
        elif not has_horizontal_scrollbars and has_vertical_scrollbars:
            return AnalyserResult.with_anomaly({"cause": "Vertical scrollbars detected"})
        else:
            return AnalyserResult.with_anomaly({"cause": "Both horizontal and vertical scrollbars detected"})
