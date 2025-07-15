#!/bin/bash

if command -v docker &> /dev/null; then
	echo "dockear already installed"
	exit 0
fi

yay -S --needed --noconfirm docker docker-buildx docker-compose
sudo groupadd -f docker
sudo usermod -aG docker $USER
