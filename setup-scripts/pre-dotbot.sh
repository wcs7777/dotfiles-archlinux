#!/bin/bash

USERNAME=${1:-wcs}
BASEDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

pacman -Syyuu --noconfirm
# yay and dotbot dependencies
pacman -S --needed --noconfirm sudo base-devel git python

source "${BASEDIR}/create-user.sh" $USERNAME
source "${BASEDIR}/config-locales.sh"
