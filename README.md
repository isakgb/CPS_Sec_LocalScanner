# CPS Security Local Network Scanner

##### Code implemented so far:

In the network package a few files related to network scanning can be found.
 
`host.py` contains object representations of hosts and ports which is used by the network scanner.

`networkinterface.py` contains an object representation of network interfaces. 

`network_scanner.py` contains the actual network scanner. Create a network scanner object by calling `scanner = NetworkScanner.create()`.

This object has methods such as:

`scanner.get_network_interfaces()` which returns a list of network interface objects. (This currently only works on Windows set to English language. We will start using linux and fix this.)

`scanner.scan_network(nif, port_scan=False)` which takes a network interface as an argument and port_scan as an optional argument and returns a list of Host objects.

`scanner.scan_network_callback(nif, callback, port_scan=False)` is similar to the aboce except it also takes a callback function as an argument. The scan will run asynchronously in a new thread and call the callback function with the result when it is done. This is useful as it prevent the scan from blocking the main thread.

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
