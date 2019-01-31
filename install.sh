#!/bin/sh

VERSION="2.1"
COMMAND="bustw"
REPO_URL="https://github.com/PinLin/bustw_cli"


main() {
    # Remove old one
    if [ -d ~/.$COMMAND ]
    then
        rm -rf ~/.$COMMAND
    fi
    
    # Clone repo to local
    if command -v wget > /dev/null
    then
        wget -O /tmp/$COMMAND-$VERSION.zip $REPO_URL/archive/v$VERSION.zip
    else
        curl -o /tmp/$COMMAND-$VERSION.zip -L $REPO_URL/archive/v$VERSION.zip
    fi
    if [ $? != 0 ]
    then
        echo "Failed to download $COMMAND."
        return 1
    fi
    unzip /tmp/$COMMAND-$VERSION.zip -d ~
    mv ~/$COMMAND-$VERSION ~/.$COMMAND

    # Create execute file
    mkdir ~/.$COMMAND/dist
    cd ~/.$COMMAND/dist
    sed "s={{path}}=~/.$COMMAND=g" ~/.$COMMAND/$COMMAND.sh > $COMMAND
    chmod +x $COMMAND

    # Create alias
    if ! command -v ${COMMAND} > /dev/null; then
        for rc in ".zshrc" ".bash_profile" ".bashrc"
        do
            if [ -f "$HOME/$rc" -o $rc = ".bashrc" ]
            then
                echo "\nalias ${COMMAND}='~/.${COMMAND}/run.py'" >> $HOME/$rc
            fi
        done
    fi
    
    # Finished
    echo
    echo Done! $COMMAND was installed.
}

main
