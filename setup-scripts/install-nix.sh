#!/bin/bash

if command -v nix &> /dev/null; then
	echo "nix already installed"
	exit 0
fi

sh <(curl --proto '=https' --tlsv1.2 -L https://nixos.org/nix/install) --daemon

mkdir -p ~/.config/nix
echo 'experimental-features = nix-command flakes' >> ~/.config/nix/nix.conf
