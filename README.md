<h1>IPVanish-Linux</h1>
<p>A Web-GUI for OpenVPN with IpVanish on Linux.</p>

<h2>Description</h2>
<p>This project is a simple web interface for OpenVPN with IpVanish on Linux. Using the CLI is a bit cumbersome, and this project aims to make it easier to connect to IpVanish servers.</p>

<h2>Features</h2>
    <ul>
        <li>🌐 Connect to IpVanish servers</li>
        <li>🔒 Authenticate using Username and Password</li>
        <li>🗺️ Country, City, and Server selection</li>
        <li>📊 Real-time connection status and network information</li>
        <li>🐍 Pure Python implementation + OpenVPN</li>
    </ul>

<h2>Installation</h2>

```bash
sudo apt-get install openvpn
git clone https://github.com/amarnathcjd/ipvanish-linux.git
cd ipvanish-linux

pip3 install -r requirements.txt
python3 main.py
```

<h2>Environment Variables</h2>
    <table>
        <thead>
            <tr>
                <th>Variable</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>USERNAME</code></td>
                <td>IpVanish Username</td>
            </tr>
            <tr>
                <td><code>PASSWORD</code></td>
                <td>IpVanish Password</td>
            </tr>
        </tbody>
    </table>

<h2>Development</h2>
<p>Want to contribute? Great! 🎉</p>

<h2>Disclaimer</h2>
<p>This project is not affiliated with IpVanish in any way. Use at your own risk. ⚠️</p>

<h2>License</h2>
<p>This project is licensed under the MIT License - see the LICENSE file for details. 📄</p>
