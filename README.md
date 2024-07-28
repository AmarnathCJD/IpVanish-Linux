<h1>IPVanish-Linux</h1>
<p>A Web-GUI for OpenVPN with IpVanish on Linux.</p>

<h2>description</h2>
<p>This project is a simple web interface for OpenVPN with IpVanish on Linux. Using the CLI is a bit cumbersome, and this project aims to make it easier to connect to IpVanish servers.</p>

<h3>features</h3>
    <ul>
        <li>🌐 connect to IpVanish servers</li>
        <li>🔒 authenticate using Username and Password</li>
        <li>🗺️ country, City, and Server selection</li>
        <li>📊 real-time connection status and network information</li>
        <li>🐍 pure Python implementation + OpenVPN</li>
    </ul>

<h3>demo screenshot</h3>
<img src='https://envs.sh/iYp.png'>

<h3>installation</h3>

```bash
sudo apt-get install openvpn
git clone https://github.com/amarnathcjd/ipvanish-linux.git
cd ipvanish-linux

pip3 install -r requirements.txt
python3 main.py
```

<h3>environment variables</h3>
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
                <td>IPVanish Username</td>
            </tr>
            <tr>
                <td><code>PASSWORD</code></td>
                <td>IPVanish Password</td>
            </tr>
            <tr>
                <td><code>INTERFACE_NAME</code></td>
                <td>Name of Network device (for speed measure)</td>
            </tr>
        </tbody>
    </table>

<h3>Disclaimer</h3>
<p>This project is not affiliated with IpVanish in any way. Use at your own risk. ⚠️</p>

<h2>License</h2>
<p>want to contribute? Great! 🎉
this project is licensed under the MIT License - see the LICENSE file for details. 📄</p>
