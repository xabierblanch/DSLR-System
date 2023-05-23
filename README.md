# High Resolution Photogrammetric System
Author: Xabier Blanch<br/>
Contact: xabierblanch@gmail.com<br/>

Codes and scripts programmed for the correct operation of High Resolution systems installed in Puigcercós (NE Spain) and in the Alhambra de Granada (S Spain).

Codes developed as part of a doctoral research at Universtiy of Barcelona (PhD). All these codes are developed for a particular case, some modifications will be necessary. If you use these codes or if they inspire you in your work, please share it with me :D (And cite it correctly).

How to cite:
-----
* Pending publication (High-end photogrammetric system)

PhD Thesis:

* Blanch, X., 2022. Developing Advanced Photogrammetric Methods for Automated Rockfall Monitoring. Doctoral dissertation. Universitat de Barcelona. Retrieved from: http://hdl.handle.net/10803/675397

Image:
-----
![Figure_II_FIG_02 copia 3](https://user-images.githubusercontent.com/37353398/151873855-66d69965-a4b9-4af0-9ee3-68e602322394.jpg)

Usage
-----

* [main.py](main.py) -> Main code (executes camera control and photo uploading)

Raspberry auxiliary codes (sh format)

* [force_shutdown.sh](force_shutdown.sh)
* [logs.sh](logs.sh)
* [run.sh](run.sh)

Main code will perfom the following actions:
---

1. Identify the cameras connected to the system.
2. Create the necessary folders for file transfer and backup.
3. Capture images using either the Sony or Canon camera (based on the identified camera).
4. Rename the captured files based on the capture count.
5. Upload the files to Dropbox using the provided token.
6. Move the uploaded files to the backup folder.
7. Delete files older than 2 days from the backup folder.

Logs.sh will perform the following action:
---
1. The script will copy the WittyPi log file to the specified folder (`/home/pi/logs` by default) and upload it to the "/log" folder in your Dropbox account.


Contribute
-----
Contributions are always welcome!
Feel free to contact me: xabierblanch@gmail.com

License
-----
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)<br/><br/>
[![CC0](https://licensebuttons.net/i/cc-gift-guide/by-sa.png)](https://creativecommons.org/licenses/by-sa/4.0/)
