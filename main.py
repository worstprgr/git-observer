#!/bin/env python
from GitObserver import GitObserver
import datetime
import time


if __name__ == '__main__':
    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} Starting git log observer...")
    observer = GitObserver()
    while 1:
        observer.run()
        time.sleep(60)
