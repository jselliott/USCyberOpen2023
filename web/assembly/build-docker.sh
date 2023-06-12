#!/bin/bash
docker rm -f uscg_web_assembly
docker build --tag=uscg_web_assembly .
docker run -p 1337:1337 --rm --name=uscg_web_assembly uscg_web_assembly