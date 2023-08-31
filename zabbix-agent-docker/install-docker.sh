#!/bin/bash

## Uninstall any such older versions before attempting to install a new version

sudo apt-get remove docker docker-engine docker.io containerd runc -y

## Update the apt package index and install packages to allow apt to use a repository over HTTPS:

sudo apt-get update -y
sudo apt-get install ca-certificates curl gnupg -y

## Add Docker’s official GPG key

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

## set up the repository

echo \
"deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
"$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

## Install Docker Engine

sudo apt-get update -y
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
