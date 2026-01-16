#!/bin/bash

set -e
set -v

rm ./dist -rf
uv run poe build
ls dist | grep a2a_registry_web_api > dist/requirements.txt

cp .env.dev dist/.env
cp -r config dist
cp -rf publish/* dist

set +v
set +e
