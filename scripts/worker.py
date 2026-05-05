#!/usr/bin/env python3
"""Worker process: polls sqlite queue and runs jobs."""
import time
import argparse
from src.queue.queue import Queue
from src.queue.jobs import process_license

HANDLERS = {
    'process_license': process_license
}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--db', default='queue.db', help='Path to sqlite db')
    p.add_argument('--sleep', type=float, default=0.5)
    args = p.parse_args()
    q = Queue(args.db)
    print('Worker started, db=', args.db)
    try:
        while True:
            processed = q.process_one(HANDLERS)
            if not processed:
                time.sleep(args.sleep)
    except KeyboardInterrupt:
        print('Worker exiting')

if __name__ == '__main__':
    main()
