(google translate rocks!)

About apk_binder_script
-----------------------
en:
apk_binder_script allows us to join two into one unifying apk resources, classes and manifest. Implements a receiver acting loader 
of the class specified. The loader takes the load of the class based on two events currently implemented: 

* android.intent.action.BOOT_COMPLETED 
* android.intent.action.ACTION_POWER_CONNECTED 

You can add actions and permissions as desired. 

In short, allows us to "extend" the functionality of a apk with us to design.

-----------------------
es:
apk_binder_script nos permite unir dos apk en uno unificando recursos, clases y manifiesto. Implementa un receiver que actúa de loader
de la clase especificada. El loader realiza la carga de la clase en base a dos eventos actualmente implementados:

* android.intent.action.BOOT_COMPLETED
* android.intent.action.ACTION_POWER_CONNECTED

Se pueden agregar acciones y permisos según se desee.

En resumen, nos permite "extender" las funcionalidades de un apk con el que nosotros diseñemos.

Requirements
------------
en:
apk_binder_script is developed in python and is tested on Windows and Linux. 
Requires apktool (included in the package) and therefore also of Java.

-----------------------
es:
apk_binder_script está desarrollado en python y está probado en Windows y Linux.
Requiere de apktool(incluído en el paquete) y por lo tanto también de Java.

Operation
---------
en:
* Decompiles apk target and binder. 
* AndroidManifest.xml unifies the two apk's. 
* Copy resources and assets (see limitations). 
* Implements a receiver that gives high on the apk target acts "binder" and reacts when the charger is connected and restart the device. 
* When the receiver "awake", invokes the case defined in the properties (which preferably should be a service). 
* The receiver and the properties are copied to the "package" target with random names. 
* Compiles and generates an apk with the merger.
* The apk is not aligned and is not signed.

-----------------------
es:
* Decompila apk objetivo y apk binder.
* Unifica AndroidManifest.xml de los dos apk's.
* Copia recursos y activos (ver limitaciones).
* Implementa un receiver que dá de alta en el apk objetivo que actúa de "binder" y que reacciona cuando se conecta el cargador y reinicia el dispositivo.
* Cuando el receiver "despierta", invoca a la case definida en el properties (que preferiblemente debe de ser un servicio).
* El receiver y el properties son copiados en el "package" objetivo con nombres aleatorios.
* Compila y genera un apk con la fusión realizada.
* El apk está no está alineado y no está firmado.

Usage
-----
en:
python ./apk_binder_script apk_target.apk apk_bind.apk class.in.apk_bind_to_invoke
If no problems are found the result is stored in "Bind_apk_target.apk"

-----------------------
es:
python ./apk_binder_script apk_target.apk apk_bind.apk class.in.apk_bind_to_invoke
Si no surgen problemas el resultado es almacenado en "Bind_apk_target.apk"

Limitations
-----------
en:
apk_binder_script has certain limitations and currently runs stably with services "bindeados" 
You may also "bindear" activities but to copy the resources from it to the destination, you may 
some left out to these already exist in the destination and therefore when activities are invoked fail. 
For example, try "bindear" meterpreter is generated correctly, but the invoke activity to generate the reverse shell, 
fails to find the requested resources. 
Viability and use cases for successful implementation are studied.

-----------------------
es:
apk_binder_script tiene ciertas limitaciones y actualmente funciona estable con servicios "bindeados".
Es posible también "bindear" actividades pero al copiar los recursos desde éste hacia el destino, es posible que
algunos se queden fuera al ya existir éstos en el destino y por lo tanto cuando las actividades son invocadas fallan.
Por ejemplo, al intentar "bindear" meterpreter, se genera correctamente, pero al invocar a la actividad para generar la shell inversa,
falla al no encontrar los recursos solicitados.
Se etudia la viabilidad y casos de uso para una correcta implementación.

Files
-----
en:
* apk_binder_script.py - script 
* tmp/ - temporary directory to store the decompiled / compiled apks 
* loader/permissions.xml - base permissions used by the loader (can be extended and register those who need it) 
* loader/receiver.xml - receiver will be discharged in order to receive AndroidManifest.xml events held there (can be extended) 
* loader/smali/Loader.smali - class implementing the receiver which in turn invoke the properties declared in the class. 
* loader/smali/Loader.java - source code receiver.
* loader/assets/loader.properties - properties containing the class to be invoked by the receiver. 
* apktool/ - directory containing the tools apktool decompile / compile apk's.

-----------------------
es:
* apk_binder_script.py - script
* tmp/ - directorio temporal donde almacenar los apks decompilados/compilados
* loader/permissions.xml - permisos base usados por el loader (pueden extenderse y darse de alta los que se necesiten)
* loader/receiver.xml - receiver que será dado de alta en el AndroidManifest.xml objetivo que recibirá los eventos ahí declarados (también * puede extenderse)
* loader/smali/Loader.smali - clase que implementa el receiver y que a su vez invocará a la clase declarada en el properties.
* loader/smali/Loader.java - código fuente del receiver.
* loader/assets/loader.properties - properties que contiene la clase que será invocada por el receiver.
* apktool/ - directorio que contiene la herramienta apktool para decompilar/compilar apk's.

Credits
-------

* Adrián Ruiz
* w: funsecurity.net
* t: @funsecurity.net
* e: adrian_adrianruiz.net
* GPG ID: 0x586270E8
