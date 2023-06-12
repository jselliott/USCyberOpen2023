#!/bin/bash
docker rm -f uscg_web_gol
docker build --tag=uscg_web_gol .
docker run -p 1337:80 --rm --name=uscg_web_gol uscg_web_gol