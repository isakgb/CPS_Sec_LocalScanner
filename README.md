# CPS Security Local Network Scanner

#### Before use:

Create a file `usersettings.json` in the main directory which should look like this:
```
{
  "interface": "<name of interface for local network>",
  "mon_disabled_interface": "<name of interface to use for monitor mode e.g. wlan0>",
  "mon_enabled_interface": "<name of interface name for monitoring when its enabled e.g wlan0mon>",
  "ap_mac_address": "<mac address of access point for deauth attack. find with iwconfig>"
}
```

##### Code implemented:

In the network package a few files related to network scanning can be found.
 
`host.py` contains object representations of hosts and ports which is used by the network scanner.

`networkinterface.py` contains an object representation of network interfaces. 

`network_scanner.py` contains the actual network scanner. Create a network scanner object by calling `scanner = NetworkScanner()`.

This object has methods such as:

`scanner.get_network_interface()` which returns the correct network interface object as specified in `usersettings.json`.

`scanner.scan_network(nif, port_scan=False)` which takes a network interface as an argument and port_scan as an optional argument and returns a list of Host objects.

`scanner.scan_network_callback(nif, callback, port_scan=False)` is similar to the aboce except it also takes a callback function as an argument. The scan will run asynchronously in a new thread and call the callback function with the result when it is done. This is useful as it prevent the scan from blocking the main thread.

`deauth.py` contains functionality to deauthenticate devices from the network. This requires a network card that supports monitor
mode. Sending deauthentication packets requires the network card to be changed into monitor mode, which will disconnect it from
the internet. Because of this it is ideal to use a separate network card for monitor mode as this prevent interruptions in
internet connectivity.

In the util package there are some classes related to storing local data and for accessing the macvendors.com API.

`history.py` contains results of previous network scans use to show historical data.

`macvendor.py` contains code for accessing the macvendors.com API as well as storing the past lookups in a file to prevent
unnecessary API calls due to the low rate limit of the API.

`usersettings.py` contains user configurable settings stored in usersettings.json which tells the program which network 
interfaces to use and which AP to use for deauth packets.

`whitelist.py` contains semiwhitelist information and stores which devices are allowed to open which ports.

 # GUI
 
 #### code implemented so far:
 
 'Home_IoT_Security.py' contains codes implementing GUI.
 
 This object has methods such as:
 'initUI()' which makes basic GUI : statusbar which shows date & time, ListWidget, ListWidgetItem, Buttons, Labels and window
 
 There are some functions that respond to the click buttons.
 The MessageBox displayed when clicked depends on the status of the list item.
 
 - We've not yet connected the actual data with the GUI. (This is a virtual list.)
 - we plan to add a function that allows users to view detailed information of device when user double-clicks an item of list.
 - The function of the scan button and the history button has not yet been implemented.
 
 
 #### Version
 - Python 3.6.10
 - pyqt 5.9.2
 
 
 #### Plans (June 4, 2020. ~)
 - We will solve the problem about encoding error by using virtual-box or another method.
 - We will connect scanning code with GUI code.
 - We will implement a function to disconnect devices by using 'aircrack-ng'
