#!/bin/bash
docker rm -f uscg_misc_on_target
docker build --tag=uscg_misc_on_target .
docker run -p 1337:1337 --rm --name=uscg_misc_on_target uscg_misc_on_target