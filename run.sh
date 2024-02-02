#!/bin/bash

BASE="$1"
OUTPUT="$2"
RADIUS="$3"
mkdir -p $OUTPUT

docker run --rm -it \
  --volume "$OUTPUT:/output" \
  --volume "$BASE:/base" \
  -e "WORLD_RADIUS=$RADIUS" \
  mc-world-generator
