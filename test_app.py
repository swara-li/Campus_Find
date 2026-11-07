
import unittest
import tempfile
from pathlib import Path

import app as campus_app


class CampusFindTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        campus_app.DATABASE = Path(self.temp_dir.name) / "test.db"
        campus_app.initialize_database()

        campus_app.app.config["TESTING"] = True
        self.client = campus_app.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "healthy")

    def test_add_report(self):
        response = self.client.post("/api/reports", json={
            "item_name": "Test Notebook",
            "report_type": "Lost",
            "category": "Stationery",
            "location": "Library",
            "contact": "test@example.com"
        })

        self.assertEqual(response.status_code, 201)

    def test_missing_required_field(self):
        response = self.client.post("/api/reports", json={
            "item_name": "Test Notebook"
        })

        self.assertEqual(response.status_code, 400)

    def test_invalid_report_type(self):
        response = self.client.post("/api/reports", json={
            "item_name": "Test Notebook",
            "report_type": "Unknown",
            "category": "Stationery",
            "location": "Library",
            "contact": "test@example.com"
        })

        self.assertEqual(response.status_code, 400)

    def test_search_reports(self):
        self.client.post("/api/reports", json={
            "item_name": "Blue Notebook",
            "report_type": "Lost",
            "category": "Stationery",
            "location": "Library",
            "contact": "test@example.com"
        })

        response = self.client.get("/api/reports?q=Notebook")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]["item_name"], "Blue Notebook")

    def test_filter_reports(self):
        self.client.post("/api/reports", json={
            "item_name": "Black Bag",
            "report_type": "Lost",
            "category": "Bags",
            "location": "Classroom",
            "contact": "test@example.com"
        })

        self.client.post("/api/reports", json={
            "item_name": "Blue Bottle",
            "report_type": "Found",
            "category": "Bottle",
            "location": "Library",
            "contact": "test@example.com"
        })

        response = self.client.get("/api/reports?type=Found")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]["report_type"], "Found")
    def test_contact_is_not_public(self):
        self.client.post("/api/reports", json={
            "item_name": "Blue Notebook",
            "report_type": "Lost",
            "category": "Stationery",
            "location": "Library",
            "contact": "private@example.com"
        })

        response = self.client.get("/api/reports")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertNotIn("contact", response.json[0])
        
    def test_resolve_report(self):
        response = self.client.post("/api/reports", json={
            "item_name": "Test Bag",
            "report_type": "Lost",
            "category": "Bags",
            "location": "Classroom",
            "contact": "test@example.com"
        })

        report_id = response.json["id"]

        resolved = self.client.patch(
            f"/api/reports/{report_id}/resolve"
        )

        self.assertEqual(resolved.status_code, 200)


if __name__ == "__main__":
    unittest.main()
