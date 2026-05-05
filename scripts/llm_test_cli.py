#!/usr/bin/env python3
import argparse
import json
from ui.backend.llm_api import init_manager, get_manager

EXAMPLE_CFG = {
    'backends': [
        {'type': 'mock', 'name': 'mock1', 'delay': 0},
    ]
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--backend', '-b', default='mock1')
    p.add_argument('--model', '-m', default='test-model')
    p.add_argument('--prompt', '-p', default='Hello world')
    args = p.parse_args()
    init_manager(EXAMPLE_CFG)
    mgr = get_manager()
    res = mgr.generate(args.backend, args.model, args.prompt)
    print(json.dumps(res, indent=2))

if __name__ == '__main__':
    main()
