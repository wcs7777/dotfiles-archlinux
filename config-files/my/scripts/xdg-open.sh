#!/bin/bash

escape_for_powershell() {
	local input="$1"
	# Escape backticks, single quotes, and double quotes
	echo "$input" | sed -e 's/`/``/g' -e "s/'/''/g" -e 's/"/\\"/g'
}

arg="$1"

if [[ -e "$arg" ]]; then
	win_path=$(wslpath -wa "$arg")
	pwsh.exe -NonInteractive -NoProfile -Command "Invoke-Item '$win_path'"
else
	url=$(echo "$arg" | sed -e 's/`/``/g' -e "s/'/''/g" -e 's/"/\\"/g')
	pwsh.exe -NonInteractive -NoProfile -Command "Start-Process '$url'"
fi
