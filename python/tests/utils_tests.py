from pathlib import Path
import subprocess
import time
import unittest

import python.utils.actor
import python.utils.client


class ClientTest(unittest.TestCase):
    def setUp(self):
        # carla_bin = Path('Simulators/Carla-0.9.9/CarlaUE4.sh')
        # home_dir = Path.home()
        # print(home_dir / carla_bin)
        # subprocess.Popen(
        #     [
        #         'bash',
        #         str(home_dir / carla_bin),
        #         '-windowed',
        #         '-ResX=1280',
        #         '-ResY=720',
        #         '-fps=60'
        #     ],
        #     stdout=subprocess.PIPE,
        #     stderr=subprocess.PIPE
        # )
        # time.sleep(10.0)
        self.host = 'localhost'
        self.port = 2000
        self.timeout = 10.0
        self.map_name = 'Town04'
        self.client = python.utils.client.create(
            self.host,
            self.port,
            self.timeout,
            self.map_name
        )

    def tearDown(self):
        self.client = None

    def test_create(self):
        carla_map = self.client.get_world().get_map()
        # self.assertEqual(self.client.get_timeout(), self.timeout)
        self.assertEqual(carla_map.name, self.map_name)


