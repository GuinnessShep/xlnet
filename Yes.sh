#!/bin/bash

# Exit on error
set -e

# Install dependencies
echo "Installing dependencies..."
brew install git python perl

# Clone the Node.js repository
echo "Cloning Node.js repository..."
git clone https://github.com/nodejs/node.git
cd node

# Set target to iOS and specify architecture (ARM64)
echo "Setting target and architecture..."
export GYP_DEFINES="OS=ios"
export ARCHS="arm64"

# Configure build
echo "Configuring build..."
./configure --dest-cpu=arm64 --cross-compiling

# Build Node.js
echo "Building Node.js..."
make

# Optionally, create an iOS framework (This step is left as a placeholder)
# You can add commands here to create an iOS framework if needed

echo "Build complete."

# Note: The resulting build will need to be transferred to an iOS device for testing.
