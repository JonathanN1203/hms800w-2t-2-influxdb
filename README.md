# Hoymiles HM800W-2T Data Collection

This is a script which is collecting the Outputpower of a HMS800W-2T.

**Disclaimer: This library is not affiliated with Hoymiles. It is an independent project developed to provide tools for interacting with Hoymiles HMS-XXXXW-2T series micro-inverters featuring integrated WiFi DTU. Any trademarks or product names mentioned are the property of their respective owners.**

## Supported Devices

The library was successfully tested with:
- Hoymiles HMS-800W-2T


## Setup

Install both libraries and adjust the variables in lines 6 to 13.

```
pip3 install hoymiles-wifi
pip3 install influxdb
```

## Run the Script

After the installation of the packaged you need to run the script with python

```
python3 collect_data.py
```

## Attribution

A special thank you for the libary and to:
- [suaveolent](https://github.com/suaveolent/): [hoymiles-wifi](https://github.com/suaveolent/hoymiles-wifi)
