#!/bin/sh

VERSION="2.1"
COMMAND="bustw"
REPO_URL="https://github.com/PinLin/bustw_cli"


main() {
    REPO_NAME=$(echo $REPO_URL | rev | cut -d '/' -f 1 | rev)

    # Remove old one
    if [ -d ~/.$COMMAND ]
    then
        rm -rf ~/.$COMMAND
    fi

    # Clone repo to local
    if command -v wget > /dev/null
    then
        wget -O /tmp/$REPO_NAME-$VERSION.zip $REPO_URL/archive/v$VERSION.zip
    else
        curl -o /tmp/$REPO_NAME-$VERSION.zip -L $REPO_URL/archive/v$VERSION.zip
    fi
    if [ $? != 0 ]
    then
        echo "Failed to download $REPO_NAME."
        return 1
    fi
    unzip /tmp/$REPO_NAME-$VERSION.zip -d ~
    mv ~/$REPO_NAME-$VERSION ~/.$COMMAND

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
