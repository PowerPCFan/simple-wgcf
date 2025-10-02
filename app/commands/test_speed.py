import math
import sys
import threading
import time
import modules.color as color
from modules.speedtest import CloudflareSpeedtest, TestResult


class Spinner:
    """
    A simple spinner.

    This is 100% chatgpt btw
    """

    spinner_chars: list[str]

    def __init__(self, delay: float = 0.1) -> None:
        self.spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.delay: float = delay
        self.running: bool = False
        self._thread: threading.Thread | None = None

    def _spin(self) -> None:
        i: int = 0
        while self.running:
            sys.stdout.write('\r' + self.spinner_chars[i % len(self.spinner_chars)] + ' ')
            sys.stdout.flush()
            time.sleep(self.delay)
            i += 1
        sys.stdout.write('\r  ')  # clear spinner
        sys.stdout.flush()

    def start(self) -> None:
        if not self.running:
            self.running = True
            self._thread = threading.Thread(target=self._spin)
            self._thread.start()

    def stop(self) -> None:
        if self.running:
            self.running = False
            if self._thread is not None:
                self._thread.join()


def test_speed_command() -> None:
    print(color.blue("Running speed test..."))

    spinner = Spinner()
    spinner.start()

    speedtest = CloudflareSpeedtest()
    results = speedtest.run_all()

    meta = results["meta"]
    tests = results["tests"]

    for key in list(tests.keys()):
        if key.endswith("_bps"):
            new_key = key.replace("_bps", "_mbps")  # make new key name by replacing _bps with _mbps
            # new_value = tests[key].value / 1e6  # convert bps value to mbps
            new_value = math.ceil(tests[key].value / 1e6)

            tests[new_key] = TestResult(value=new_value, time=tests[key].time)  # make new mbps key
            tests.pop(key)  # remove old bps key

    # meta
    location = f"{meta['location_city'].value}, {meta['location_region'].value}"  # ex: San Francisco, California
    ip = meta["ip"].value  # ex: 192.168.1.1

    # tests
    down_100kB_mbps = tests["100kB_down_mbps"].value
    up_100kB_mbps = tests["100kB_up_mbps"].value

    down_1MB_mbps = tests["1MB_down_mbps"].value
    up_1MB_mbps = tests["1MB_up_mbps"].value

    down_10MB_mbps = tests["10MB_down_mbps"].value
    up_10MB_mbps = tests["10MB_up_mbps"].value

    down_25MB_mbps = tests["25MB_down_mbps"].value
    # no up for this one

    down_90th_percentile_mbps = tests["90th_percentile_down_mbps"].value
    up_90th_percentile_mbps = tests["90th_percentile_up_mbps"].value

    isp = tests["isp"].value
    jitter = tests["jitter"].value
    latency = tests["latency"].value

    spinner.stop()

    print(color.green("\nResults:"))

    print(color.blue("\nConnection Information:"))
    print(f"IP: {ip}")
    print(f"Location: {location}")
    print(f"ISP: {isp}")

    print(color.blue("\n\nSpeed Test Results:"))
    print(f"Download Speed (100 kB): {down_100kB_mbps} Mbps")
    print(f"Upload Speed (100 kB): {up_100kB_mbps} Mbps")
    print()
    print(f"Download Speed (1 MB): {down_1MB_mbps} Mbps")
    print(f"Upload Speed (1 MB): {up_1MB_mbps} Mbps")
    print()
    print(f"Download Speed (10 MB): {down_10MB_mbps} Mbps")
    print(f"Upload Speed (10 MB): {up_10MB_mbps} Mbps")
    print()
    print(f"Download Speed (25 MB): {down_25MB_mbps} Mbps")
    print()
    print(f"90th Percentile Download Speed: {down_90th_percentile_mbps} Mbps")
    print(f"90th Percentile Upload Speed: {up_90th_percentile_mbps} Mbps")

    print(color.blue("\n\nQuality Metrics:"))
    print(f"Jitter: {jitter} ms")
    print(f"Latency: {latency} ms")
