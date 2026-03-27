#!/bin/bash
# Production build script for static site generator
# Usage: ./build.sh [REPO_NAME]

REPO_NAME=${1:-"static-site-generator"}

echo "Building site for production..."
python3 src/main.py "/$REPO_NAME/"
echo "Site built successfully!"
