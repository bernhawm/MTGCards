#!/bin/bash
set -e

# Activate venv
source venv/Scripts/activate

# Step 1: Update local cards.json from Scryfall
echo "Updating cards.json from Scryfall..."
python init/UpdateCardList.py

# Step 2: Build the Docker image
echo "Building Docker image..."
docker build -t mtg-postgres .

# Step 3: Run the container
echo "Running Docker container..."
docker run -d \
  --name mtg-db \
  -p 5432:5432 \
  -e POSTGRES_PASSWORD=yourpassword \
  mtg-postgres

echo "Done. PostgreSQL container 'mtg-db' is running on port 5432."
