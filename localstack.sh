#!/usr/bin/env bash
set -e
pip3 install localstack[full]
localstack start
