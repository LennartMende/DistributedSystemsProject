import importlib.util
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

spec = importlib.util.spec_from_file_location("mqtt_utils", Path(__file__).resolve().parent / "utils.py")
utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(utils)


class UtilsCertPathTests(unittest.TestCase):
    def test_temp_publisher_cert_files_exist(self):
        cfg = utils.ClientCfg(client_id="leader_temp_publisher")
        self.assertTrue(Path(cfg.cert).exists(), f"Missing cert: {cfg.cert}")
        self.assertTrue(Path(cfg.key).exists(), f"Missing key: {cfg.key}")


if __name__ == "__main__":
    unittest.main()
