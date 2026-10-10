#!/usr/bin/env python3
"""Offline structural checks for the staged transcription docs and OpenAPI wiring."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
spec = json.loads((ROOT / 'api-reference/openapi.json').read_text())
nav = json.loads((ROOT / 'docs.json').read_text())


def references(value):
    if isinstance(value, dict):
        for key, item in value.items():
            if key == '$ref' and item.startswith('#/'):
                target = spec
                for part in item[2:].split('/'):
                    target = target[part.replace('~1', '/').replace('~0', '~')]
            references(item)
    elif isinstance(value, list):
        for item in value:
            references(item)


references(spec)
for page in ('cloud/grid/transcription', 'api-reference/grid-transcriptions-reserve',
             'api-reference/grid-transcriptions'):
    text = (ROOT / (page + '.mdx')).read_text()
    assert page in json.dumps(nav), 'Missing navigation: ' + page
    for method, route in re.findall(r"openapi:\s*['\"]([A-Z]+) ([^'\"]+)", text):
        assert method.lower() in spec['paths'][route]
    for route in re.findall(r'\]\((/[^)#]+)', text):
        assert (ROOT / (route[1:] + '.mdx')).exists(), 'Broken link: ' + route

for route in ('/v1/audio/transcriptions/reserve', '/v1/audio/transcriptions'):
    operation = spec['paths'][route]['post']
    schema = operation['requestBody']['content']['application/json']['schema']
    assert schema['additionalProperties'] is False
    assert set(schema['required']) <= set(schema['properties'])
    assert 'application/json' in operation['responses']['200']['content']

reserve = spec['paths']['/v1/audio/transcriptions/reserve']['post']
request = reserve['requestBody']['content']['application/json']
for key in ('model_revision', 'model_sha256'):
    assert key in request['schema']['required']
    assert request['example'][key] in request['schema']['properties'][key]['enum']
response = reserve['responses']['200']['content']['application/json']['schema']
quote = response['properties']['quote']
assert set(quote['required']) == {'sample_count', 'audio_seconds', 'rate_usd_per_second',
    'minimum_charge_usd', 'price_usd', 'currency'}
assert set(quote['properties']) == set(quote['required'])
assert quote['properties']['currency']['enum'] == ['USDC']
assert '16 KiB' in reserve['responses']['413']['description']
usage = spec['paths']['/v1/audio/transcriptions']['post']['responses']['200']['content']['application/json']['schema']['properties']['usage']['properties']['audio_seconds']
assert usage['type'] == 'number' and usage['minimum'] == 0
assert request['schema']['properties']['sample_count']['maximum'] == 960000
assert 'X-Payment' not in [item['name'] for item in reserve['parameters']]
print('PASS JSON, internal refs, STT navigation/pages/operations/links, strict inputs, immutable pins, USDC quote')
