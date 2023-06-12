#!/bin/bash
docker rm -f uscg_web_vault
docker build --tag=uscg_web_vault .
docker run --add-host backend.vault.uscg:127.0.0.1 -p 1337:80 --rm --name=uscg_web_vault uscg_web_vault