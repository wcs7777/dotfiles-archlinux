#!/bin/bash

if command -v nvim &> /dev/null; then
	echo "nvim already installed"
	exit 0
fi
curl -SL \
	--output ~/.local/bin/nvim \
	https://github.com/neovim/neovim-releases/releases/download/v0.11.2/nvim-linux-x86_64.appimage \
	&& chmod u+x ~/.local/bin/nvim
