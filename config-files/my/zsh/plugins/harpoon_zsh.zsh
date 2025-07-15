__my_indexed_paths() {
	local paths=""
	local i
	for ((i = 1; i <= "$#__my_paths_array"; i++)) {
		paths+="${i} ${__my_paths_array[$i]}\n"
	}
	echo "$paths"
}

__my_print_paths() {
	zle .kill-buffer
	echo
	__my_indexed_paths
	echo
	zle .accept-line
}

__my_path() {
	local buffer="$BUFFER"
	zle .kill-buffer
	cd "$1"
	zle .accept-line
	print -z "$buffer"
}

__my_path_by_index() {
	__my_path "${__my_paths_array[$1]}"
}

__my_path_h() { __my_path "$HOME"    }
__my_path_1() { __my_path_by_index 1 }
__my_path_2() { __my_path_by_index 2 }
__my_path_3() { __my_path_by_index 3 }
__my_path_4() { __my_path_by_index 4 }
__my_path_5() { __my_path_by_index 5 }
__my_path_6() { __my_path_by_index 6 }
__my_path_7() { __my_path_by_index 7 }
__my_path_8() { __my_path_by_index 8 }
__my_path_9() { __my_path_by_index 9 }

__my_fpaths() {
	zle .kill-buffer
	fpaths
	zle .accept-line
}

fpaths() {
	local paths=$(__my_indexed_paths)
	local chosen="$(echo "$paths" | fzf --tac --height=~100% --select-1 --cycle)"
	if [[ -n "$chosen" ]]; then
		local i=$(echo "$chosen" | awk '{ print $1 }')
		cd "${__my_paths_array[$i]}"
	fi
}

zle -N __my_path_h
zle -N __my_print_paths
zle -N __my_path_1
zle -N __my_path_2
zle -N __my_path_3
zle -N __my_path_4
zle -N __my_path_5
zle -N __my_path_6
zle -N __my_path_7
zle -N __my_path_8
zle -N __my_path_9
zle -N __my_fpaths
