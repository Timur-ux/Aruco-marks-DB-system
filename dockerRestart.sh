#!/bin/bash

cd ./create-intro/
npm run build
cd ..
docker compose restart
