#!/bin/bash

docker compose down backend
docker compose up -d --build backend && docker compose logs backend
