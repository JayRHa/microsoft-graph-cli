import unittest
from microsoft_graph_cli.const import ENDPOINTS
from microsoft_graph_cli.transform import apply_path_params, merge_query, parse_key_value_pairs, redact_headers

class TransformTests(unittest.TestCase):
    def test_endpoint_keys_are_unique(self):
        keys = [item["key"] for item in ENDPOINTS]
        self.assertEqual(len(keys), len(set(keys)))
    def test_apply_path_params_encodes_values(self):
        self.assertEqual(apply_path_params("/users/{id}", {"id": "john.doe@example.com"}), "/users/john.doe%40example.com")
    def test_parse_key_value_pairs(self):
        self.assertEqual(parse_key_value_pairs(["$top=10"]), {"$top": "10"})
    def test_merge_query_preserves_existing_query(self):
        self.assertEqual(merge_query("/users?$top=5", {"$select": "id"}), "/users?%24top=5&%24select=id")
    def test_redact_headers(self):
        self.assertEqual(redact_headers({"Authorization": "Bearer secret"})["Authorization"], "<redacted>")

if __name__ == "__main__":
    unittest.main()
