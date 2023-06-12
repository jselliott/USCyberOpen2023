# Vault

A CTFd compatible docker image for a web challenge. Scenario:

Vagabond Vault is the newest place where hackers can post their stolen data and other illicit downloads. They seem to be using some sort of distributed setup that allows them to quickly recover when a frontend server is taken down. See what you can do to uncover the secrets behind this nefarious site!

## Setup

Run the included build-docker.sh script to build and deploy the container in docker.


## Solution

When players examine the download functionality they should see that there is an extra header that is being passed when requesting the files, "x-vault-server", indicating that there is a backend service that is being called to download files. Additionally, if they check robots.txt they will notice there is a path "/vault_key" which is disallowed and rejects them from their current IP address.

These should all be hints that there is an SSRF vulnerability that will allow them to request the vault_key from localhost instead. Using Burp Suite or some other tool, the player can modify the request headers so that x-vault-server is set to "127.0.0.1/vault_key" and it will get the password needed to decrypt the zip files with the flag.