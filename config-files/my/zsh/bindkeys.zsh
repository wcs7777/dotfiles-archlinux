__my_clear_screen() {
	zle clear-screen
	if [[ -v TMUX ]]; then
		tmux clear-history
	fi
}

zle -N __my_clear_screen

# bindkey "^H"      backward-kill-word # ctrl-backspace
bindkey "^L"      __my_clear_screen  # ctrl-l
bindkey "^[[3;5~" kill-word          # ctrl-del
bindkey "^[[1~"   beginning-of-line  # home
bindkey "^[[4~"   end-of-line        # end
bindkey "^[[3~"   delete-char        # del
bindkey "^[[1;5C" forward-word       # ctrl-right
bindkey "^[[1;5D" backward-word      # ctrl-left
bindkey "^@"      autosuggest-accept # ctrl-space

bindkey "^[h" __my_path_h
bindkey "^[0" __my_fpaths
bindkey "^[1" __my_path_1
bindkey "^[2" __my_path_2
bindkey "^[3" __my_path_3
bindkey "^[4" __my_path_4
bindkey "^[5" __my_path_5
bindkey "^[6" __my_path_6
bindkey "^[7" __my_path_7
bindkey "^[8" __my_path_8
bindkey "^[9" __my_path_9
