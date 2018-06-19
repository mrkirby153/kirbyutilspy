from unittest import TestCase
from kirbyutilspy import Time, TimeUnit


class TestTime(TestCase):
    def test_greater_than(self):
        self.assertTrue(TimeUnit.YEAR > TimeUnit.WEEK)

    def test_less_than(self):
        self.assertTrue(TimeUnit.SECOND < TimeUnit.YEAR)

    def test_equals(self):
        self.assertTrue(TimeUnit.SECOND == TimeUnit.SECOND)
        self.assertFalse(TimeUnit.SECOND == "Second")

    def test_fit_time(self):
        self.assertTrue(Time.fit_time(30) == TimeUnit.SECOND)
        self.assertTrue(Time.fit_time(1) == TimeUnit.SECOND)

    def test_fit_time_smallest(self):
        self.assertEquals(Time.fit_time(3600, TimeUnit.SECOND), TimeUnit.SECOND)

    def test_format_time(self):
        self.assertEquals(Time.format_time(0, 30), "30 Seconds")

    def test_format_time_multiple(self):
        self.assertEquals(Time.format_time(1, 90), "1.5 Minutes")

    def test_format_long(self):
        self.assertEquals(Time.format_time_long(10), "10 Seconds")

    def test_format_long_min_sec(self):
        self.assertEquals(Time.format_time_long(65), "1 Minute, 5 Seconds")
        self.assertEquals(Time.format_time_long(11404), "3 Hours, 10 Minutes, 4 Seconds")

    def test_parse_time_non_string(self):
        self.assertRaises(TypeError, Time.parse_time, 30)

    def test_parse_time(self):
        self.assertEquals(Time.parse_time("10m5s"), 605)

    def test_parse_time_long(self):
        self.assertEquals(Time.parse_time("10 minutes 5 seconds"), 605)

    def test_parse_time_singular(self):
        self.assertEquals(Time.parse_time("10 minutes 1 second"), 601)
