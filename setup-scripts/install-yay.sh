#!/bin/bash

if command -v yay &> /dev/null; then
	echo "yay already installed"
	exit 0
fi

current_dir=$(pwd)
temp_dir=$(mktemp -d)

cd "$temp_dir"

git clone --depth=1 https://aur.archlinux.org/yay.git
cd yay
makepkg --syncdeps --rmdeps --install --clean
cd ..
rm -rf yay

cd "$current_dir"
