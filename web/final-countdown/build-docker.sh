#!/bin/bash
docker rm -f uscg_web_countdown
docker build --tag=uscg_web_countdown .
docker run -p 1337:1337 --rm --name=uscg_web_countdown uscg_web_countdown