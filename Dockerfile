

sudo lpadmin -E -p 'HP_2055d' -v 'hp:/usb/HP_LaserJet_P2055d?serial=S171YME' 

-E: Enable the printer
-p: The name of the printer
-v: The destination URI of the printer -select from 'sudo lpinfo -v'
-m: The driver model for the printer -select from 'sudo lpinfo -m'
