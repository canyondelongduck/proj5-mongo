"""
Tests for the Submit and Display buttons.
Run inside the container:  docker compose exec web python tests.py
Uses a separate 'controls_test' collection so real data is untouched.
"""
import unittest
import flask_brevets as fb


class ButtonTests(unittest.TestCase):
    def setUp(self):
        fb.collection = fb.db.controls_test
        fb.collection.delete_many({})
        self.client = fb.app.test_client()

    def tearDown(self):
        fb.collection.delete_many({})

    # ---- Submit ----
    def test_submit_empty_returns_error(self):
        r = self.client.post("/_submit", json={"controls": []})
        self.assertEqual(r.status_code, 400)
        self.assertIn("error", r.get_json())

    def test_submit_missing_times_returns_error(self):
        r = self.client.post("/_submit", json={"controls": [
            {"km": "100", "open": "", "close": ""}]})
        self.assertEqual(r.status_code, 400)

    def test_submit_valid_then_double_submit_has_no_duplicates(self):
        body = {"brevet_dist_km": "200", "begin_time": "2017-01-01T00:00",
                "controls": [{"km": "100", "miles": "62.1",
                              "open": "Sun 1/1 2:56", "close": "Sun 1/1 6:40"}]}
        self.assertEqual(self.client.post("/_submit", json=body).status_code, 200)
        self.assertEqual(self.client.post("/_submit", json=body).status_code, 200)
        self.assertEqual(fb.collection.count_documents({}), 1)

    # ---- Display ----
    def test_display_empty_db_shows_message(self):
        r = self.client.get("/display")
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"No controle times", r.data)

    def test_display_shows_submitted_rows(self):
        self.client.post("/_submit", json={"controls": [
            {"km": "100", "open": "Sun 1/1 2:56", "close": "Sun 1/1 6:40"}]})
        r = self.client.get("/display")
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"Sun 1/1 2:56", r.data)


if __name__ == "__main__":
    unittest.main()