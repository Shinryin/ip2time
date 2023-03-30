# ip2time
ip2time is a Python tool that automatically detects and updates your system's timezone based on your external IP address. This tool is especially useful for those who travel frequently or use VPNs, as it saves time and effort required to manually change the timezone. 
- I made this program after reading https://gist.github.com/mrled/8d29fde758cfc7dd0b52f3bbf2b8f06e, and ran into the same issues myself. ip2time features a very comprehensive custom mapping of IANA timezones -> Windows timezones. Feel free to use this for any of your projects!

# Features
- Detects your external IP address.
- Provides your current location based on your IP.
- Determines your timezone based on your IP address.
- Updates your system's timezone automatically.
- Supports Windows, macOS, and Linux platforms.

# Usage
- If you download ip2time from the releases page - https://github.com/Shinryin/ip2time/releases/ - this is a fully standalone, compiled version of the program that runs without any dependencies. Basically, all you need to do is double click and program and RUN IT AS ADMINISTRATOR!

- To use ip2time after BUILDING it, simply run the script in your terminal or command prompt. Make sure you have the required Python packages installed (e.g., ctypes, platform, and requests). The script will then detect your external IP, determine your timezone, and update your system's timezone accordingly.

Requirements
Python 3.x
ctypes, platform, and requests packages
