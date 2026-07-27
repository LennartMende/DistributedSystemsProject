# Umgang auf eingebettetem Linux
Dieser Ordner ist dafür gedacht, ebenfalls eine Arbeit mit einem Client zu ermöglichen, damit es sich tatsächlich um verteilte Systeme handelt.  
In diesem Beispiel wurde ein STM32 als Client verwendet.  
Die Ordner sind, bspw. mit Hilfe von yocto, in den entsprechenden Verzeichnissen einzubringen.  
Der certs-Ordner muss eine Ebene über dem utils.py-Skript, also im selben Verzeichnis wie lerobot, liegen.  
Beispiel:
|---...lerobot
...
|---lerobot
    |---utils.py
    ...
|---certs
|---mqtt