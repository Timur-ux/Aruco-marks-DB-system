#!/bin/bash

docker compose down frontend
docker compose up --build -d frontend && docker compose logs frontend
