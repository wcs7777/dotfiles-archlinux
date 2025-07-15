# alias lazyvim="NVIM_APPNAME=snvim/lazyvim nvim"
alias deltaa="delta --no-gitconfig --config ~/.config/delta"
alias docker-rmi-dangling="docker image rm \`docker images -qa -f 'dangling=true'\`"
alias grep='grep --color=auto'
alias h1='history 1'
alias hs='history 1 | rg'
alias hsi='history 1 | rg -i'
alias list-git-ignores-files="git check-ignore -v -- *"
alias permissions="stat -c '%a %U:%G %n'"
alias rnvim="nvim -R"

clipcopy () {
	cat "${1:-/dev/stdin}" | clip.exe
}

sqlf () {
	cat "${1}" | sleek
}

mkcd() {
	mkdir -p -- "$1" && cd -P -- "$1"
}

wincd() {
	(cd "$(readlink -f ${1:-.})" && explorer.exe .)
}
