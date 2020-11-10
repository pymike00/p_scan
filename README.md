# p_scan - simple multithread tcp port scanner
Simple TCP Port Scanner. *Written with the sole purpose of having fun while making a YouTube video*.

<p align="center">
  <img alt="pscan" src="pscan.png"/>
</p>

## Install

```
git clone https://github.com/pymike00/p_scan.git
cd p_scan
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd src
python3 p_scan.py
```

By default PScan only scans for some commonly used ports, the list of which can be found in "common_ports.json".

The repo also include a "iana_tcp_ports,json" file containing an higher number of ports and their related common service.
To use this file just update the value of PORTS_DATA_FILE in the PScan class.