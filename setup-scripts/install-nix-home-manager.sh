#!/bin/bash

if command -v home-manager &> /dev/null; then
	echo "home-manager already installed"
	exit 0
fi

current_dir=$(pwd)

cd ~/.config/home-manager

nix build .#homeConfigurations."wcs".activationPackage
./result/activate

cd "$current_dir"
