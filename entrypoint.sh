#!/bin/bash

# Tini allows us to avoid several Docker edge cases, see https://github.com/krallin/tini.
/usr/bin/tini -s -- python "$@"
