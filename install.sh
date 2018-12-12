#!/bin/sh

ALIAS_NAME="bustw"
REPO_NAME="bustw_cli"
REPO_URL="https://github.com/PinLin/$REPO_NAME"

# Install application
makeInstall() {
    # Check counts of arguments
    if [ $# -lt 1 ]
    then
        return -1
    fi
    
    # Judge which is the package manager we used
    kernel=$(uname -s)
    if [ "$kernel" = "Darwin" ]
    then
        if command -v brew > /dev/null 2>&1
        then
            # macOS with brew
            brew install $1
            return $?
        else
            echo "You need to install Homebrew on your macOS before runing this script."
            echo See this: https://brew.sh
            return 87
        fi
        
    elif [ "$kernel" = "Linux" ]
    then
        if command -v lsb_release > /dev/null 2>&1
        then
            os=$(echo $(lsb_release -i | cut -d ':' -f 2))
        else
            os=''
        fi

        case $os in
            "Debian"|"Ubuntu")
                # Debian/Ubuntu with apt-get
                sudo apt-get install -y $1
                return $?
            ;;

            "Fedora"|"CentOS")
                if command -v dnf > /dev/null 2>&1
                then
                    # Fedora/CentOS with dnf
                    sudo dnf install -y $1
                    return $?
                else
                    # Fedora/CentOS with yum
                    sudo yum install -y $1
                    return $?
                fi
            ;;

            *)
                if command -v apt-get > /dev/null 2>&1
                then
                    # Embedded Device with apt-get
                    sudo apt-get install -y $1
                    return $?
                fi

                if command -v ipkg > /dev/null 2>&1
                then
                    # Embedded Device with ipkg
                    sudo ipkg install $1
                    return $?
                fi

                if command -v opkg > /dev/null 2>&1
                then
                    # Embedded Device with opkg
                    sudo opkg install $1
                    return $?
                fi
            ;;
        esac
    fi 
}


# Ask for question
askQuestion() {
    # Check counts of arguments
    if [ $# -lt 2 ]
    then
        return -1
    fi

    # Ask
    if [ "$2" = "Yn" ]
    then
        # Display question and default yes
        printf "$1 [Y/n] "; read ans
        case $ans in
            [Nn*])
                return 1
                ;;
            *)
                return 0
                ;;
        esac
    else
        # Display question and default no
        printf "$1 [y/N] "; read ans
        case $ans in
            [Yy*]) 
                return 0
                ;;
            *) 
                return 1
                ;;
        esac
    fi
}


main() {
    # Check git
    if ! command -v git > /dev/null 2>&1
    then
        echo "This installer uses git to clone the repo to localhost."
        if askQuestion "Do you want to install git?" "Yn"
        then
            makeInstall git
        fi
    fi

    # Remove old one
    if [ -d ~/.$ALIAS_NAME ]
    then
        rm -rf ~/.$ALIAS_NAME
    fi
    
    # Clone repo to local
    git clone $REPO_URL ~/.$ALIAS_NAME
    if [ $? != 0 ]
    then
        echo "Failed to clone $REPO_NAME."
        return 1
    fi

    # Check python3
    if ! command -v python3 > /dev/null 2>&1
    then
        echo "This application will run with python3."
        if askQuestion "Do you want to install python3?" "Yn"
        then
            makeInstall python3
        fi
    fi

    # Create alias
    if ! command -v ${ALIAS_NAME} > /dev/null; then
        for rc in ".zshrc" ".bash_profile" ".bashrc"
        do
            if [ -f "$HOME/$rc" -o $rc = ".bashrc" ]
            then
                echo "\nalias ${ALIAS_NAME}='~/.${ALIAS_NAME}/run.py'" >> $HOME/$rc
            fi
        done
    fi
    
    # Finished
    echo
    echo Done! $REPO_NAME was installed.
}

main
