#!/usr/bin/env python3
import json, pathlib, shutil
root = pathlib.Path(__file__).parent
assert json.loads((root / 'toolchain-lock.json').read_text())['process_id'] == 'MCLP-001'
for command in ('python', 'ffmpeg'):
    assert shutil.which(command), f'{command} missing'
print('MCLP_SMOKE_PASS')
