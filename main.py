import os

import sentry_sdk
from dotenv import load_dotenv

from controllers import login_ctrl

load_dotenv(dotenv_path=".env")

if __name__ == "__main__":
    sentry_sdk.init(
        dsn=f"{os.getenv('SENTRY_DSN')}",
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=1.0,
    )

    def slow_function():
        import time

        time.sleep(0.1)
        return "done"

    def fast_function():
        import time

        time.sleep(0.05)
        return "done"

    # Manually call start_profiler and stop_profiler
    # to profile the code in between
    sentry_sdk.profiler.start_profiler()
    for i in range(0, 10):
        slow_function()
        fast_function()
    #
    # Calls to stop_profiler are optional - if you don't stop the profiler, it will keep profiling
    # your application until the process exits or stop_profiler is called.
    sentry_sdk.profiler.stop_profiler()
    try:
        login_ctrl.LoginController.run()
    except KeyboardInterrupt:
        print("\n\x1B[37mStopped by 'service-ordered' user interruption...")
