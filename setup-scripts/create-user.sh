#!/bin/bash

USERNAME=${1:-wcs}

if id "$USERNAME" &> /dev/null; then
	echo "$USERNAME already exists"
	exit 0
fi

echo "%wheel ALL=(ALL) ALL" > /etc/sudoers.d/wheel
useradd -m -G wheel -s /bin/bash "$USERNAME"
passwd $USERNAME

cat << EOF > /etc/wsl.conf
[boot]
systemd=true

[user]
default=$USERNAME
EOF
