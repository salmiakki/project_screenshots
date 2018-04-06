from screenqual.filter.text_near_edge_detector import TextNearEdgeDetector
from tests.unit.unit_test import UnitTest


class TestTextNearEdgeDetector(UnitTest):
    def setUp(self):
        self.dtor = TextNearEdgeDetector()

    def test_does_not_fire_on_good_text_document_screenshot1(self):
        self.assert_no_anomaly(self.dtor,
                               "text_near_edge/ok.png")

    def test_does_not_fire_on_good_text_document_screenshot2(self):
        self.assert_no_anomaly(self.dtor,
                               "text_near_edge/1_14.png")

    def test_does_not_fire_on_good_text_document_screenshot3(self):
        self.assert_no_anomaly(self.dtor,
                               "text_near_edge/9_2.png")

    def test_fires_on_text_document_screenshot_with_text_crossing_horizontal_line(self):
        self.assert_has_anomaly(self.dtor,
                                "text_near_edge/horizontal.png")

    def test_fires_on_text_document_screenshot_with_text_crossing_vertical_line(self):
        self.assert_has_anomaly(self.dtor,
                                "text_near_edge/vertical.png")

    def test_fires_on_text_document_screenshot_with_picture_crossing_vertical_line(self):
        self.assert_has_anomaly(self.dtor,
                                "text_near_edge/8_3.png")

    # def test_fires_on_text_document_screenshot_with_one_letter_near_vertical_line(self):
    #     self.assert_has_anomaly(self.dtor,
    #                             "text_near_edge/8_4_4.png")

    def test_fires_on_text_document_screenshot_with_a_lot_of_text_near_vertical_line(self):
        self.assert_has_anomaly(self.dtor,
                                "text_near_edge/0_10_1.png")
