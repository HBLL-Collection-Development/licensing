#!/usr/bin/env python3
"""Enqueue sample-data files as license jobs."""
import os
from src.queue.queue import Queue

def main():
    db = 'queue.db'
    q = Queue(db)
    sample_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sample-data')
    enqueued = []
    for root, dirs, files in os.walk(sample_dir):
        for f in files:
            path = os.path.join(root, f)
            jid = q.enqueue('process_license', {'path': path})
            enqueued.append(jid)
    print('Enqueued', len(enqueued), 'jobs')

if __name__ == '__main__':
    main()
