#!/bin/bash

BASEDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "${BASEDIR}/install-nix-home-manager.sh"
chsh -s /bin/zsh
