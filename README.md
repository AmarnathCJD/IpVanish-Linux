### IpVanish Linux

A Web-GUI for OpenVPN with IpVanish on Linux.

### Description

This project is a simple web interface for OpenVPN with IpVanish on Linux. Using the cli is a bit cumbersome and this project aims to make it easier to connect to IpVanish servers.

### Features

- Connect to IpVanish servers
- Authenticate using Username and Password
- Country, City and Server selection
- Real-time connection status and network information
- Pure Python implementation + OpenVPN

### Installation

```sh
sudo apt-get install openvpn
git clone https://github.com/amarnathcjd/ipvanish-linux.git
cd ipvanish-linux

pip3 install -r requirements.txt
python3 main.py
```

### ENV Variables

| Variable | Description |
| ------ | ------ |
| USERNAME | IpVanish Username |
| PASSWORD | IpVanish Password |

### Development

Want to contribute? Great!

### Disclaimer

This project is not affiliated with IpVanish in any way. Use at your own risk.

### License

This project is licensed under the MIT License - see the LICENSE file for details.
