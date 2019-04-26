# bustw_cli
bus tracker for Taiwanese for CLI

## Demo
| `bustw`  | `bustw 680` |
| :-------------------------------------: | :-------------------------------------: |
| ![main](https://imgur.com/2WjJicz.png) | ![680](https://imgur.com/JIehNZL.png) |

| `bustw Taipei.忠孝幹線 1 1` | `bustw Taipei.72 2 2` |
| :-------------------------------------: | :-------------------------------------: |
| ![Taipei.忠孝幹線](https://imgur.com/rC6GbP2.png) | ![Taipei.72](https://imgur.com/1PM33zC.png) |

## Install
1. Install bustw_cli.
```bash
# by `curl`
sh -c "$(curl -L https://raw.githubusercontent.com/PinLin/bustw_cli/v2.1/install.sh)"

# by `wget`
sh -c "$(wget -O- https://raw.githubusercontent.com/PinLin/bustw_cli/v2.1/install.sh)"
```

2. Install dependencies.
```bash
pip3 install -r $HOME/.bustw/requirements.txt
```

## License
MIT License

## Source
[![公共運輸整合資訊流通服務平臺（Public Transport data eXchange, PTX）](https://imgur.com/wp2gOeU.png)](http://ptx.transportdata.tw/PTX)