Open Aero VTOL

Links: https://www.rcgroups.com/forums/showthread.php?1972686-OpenAeroVTOL-with-transitional-mixers-%28perfect-for-VTOLs%29
GUI: https://www.rcgroups.com/forums/showthread.php?2624242-OpenAeroVTOL-GUI
Flashtool: https://lazyzero.de/en/modellbau/kkmulticopterflashtool/start
Driver: https://zadig.akeo.ie/
Driver Instructions: https://electronics.stackexchange.com/questions/416714/avrdude-does-not-recognize-usbasp-device/417509#417509

USBASP Dongle: https://www.amazon.com/Geekstory-Microcontroller-Programmer-Downloader-Adapter/dp/B07NZ59VK2/ref=dp_prsubs_1?pd_rd_i=B07NZ59VK2&psc=1 (one of this style is needed for this flashing method)

Download Info: (windows)
- Download and extract the given zip file
- DELETE THE ZIP FILE FROM YOUR COMPUTER
- Navigate to the driver link above - download most recent version of zadig
- In zadig, press options and lsit all devices
- select usbasp
- change the driver on the right side to libusb-win32 (see driver instructions above)
- install the driver

Flashing Info:
- right click the GUI excel workbook
- click properties
- press the checkbox for security unlock under general and apply (enabled macros)
- open the GUI excel workbook
- navigate to the settings tab
- click locate new hex file
- navigate to the OAV folder and select either the regular or mini hex depending on board
- press set path to avrdude
- navigate to the OAV folder\lib\avrdude\windows and select avrdude.exe
- connect a KK2 board via the usbasp dongle and press write .hex file