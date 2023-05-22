#!/bin/bash
docker rm -f uscg_web_hacker
docker build --tag=uscg_web_hacker .
docker run -p 1337:1337 --rm --name=uscg_web_hacker uscg_web_hacker