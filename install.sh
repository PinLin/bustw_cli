#!/usr/bin/env bash

if [ -d ~/.bustw ]; then
    rm -rf ~/.bustw
fi

git clone https://github.com/PinLin/bustw_cli ~/.bustw

mkdir -p ~/.bustw/exec
cd ~/.bustw/exec
ln -s ../app.py bustw
chmod 755 bustw

if ! command -v bustw > /dev/null; then
    for rc in ".zshrc" ".bash_profile" ".bashrc"; do
        if [ -f "$HOME/$rc" ] || [ $rc == ".bashrc" ]; then
            echo >> $HOME/$rc
            echo 'export PATH="$HOME/.bustw/exec:$PATH"' >> $HOME/$rc

            echo Success! Use '`source ~/'$rc'`' to reload your shell.
        fi
    done
else
    echo 'Success! `bustw` is ready.'
fi
