(google translate rocks!)

About apk_binder_script
-----------------------
en:
apk_binder_script allows us to unify two apk's in one. This copy smali code, active and manifest. 
Implements a receiver acting loader loading the class specified as a parameter (a service). 
The original application is normally run in parallel, the service is invoked by the loader based on two events: 

* android.intent.action.BOOT_COMPLETED 
* android.intent.action.ACTION_POWER_CONNECTED 

You can add actions and permissions as desired. 
In short, allows us to "extend" the functionality of a apk, doors implement "administrative", etc.

-----------------------
es:
apk_binder_script nos permite unificar dos apk's en uno. Para ello copia código smali, activos y manifiesto. 
Implementa un receiver que actúa de loader cargando la clase que se ha especificado como parámetro (un servicio).
La aplicación original se ejecuta normalmente y en paralelo, el servicio es invocado por el loader en base a dos eventos:

* android.intent.action.BOOT_COMPLETED
* android.intent.action.ACTION_POWER_CONNECTED

Se pueden agregar acciones y permisos según se desee.
En resumen, nos permite "extender" las funcionalidades de un apk, implementar puertas "administrativas", etc.

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
* Decompiles apk apk objective and binder. 
* AndroidManifest.xml unifies the two apk's. 
* Copy and smali code assets (other resources, see limitations). 
* Implements a receiver that gives high on the apk objective acts "binder" and reacts when the charger is connected or restart the device. 
* When the receiver "awake", invokes the class defined in the properties (it must be a service). 
* The receiver and the properties are copied to the "package" target with random names. 
* Compiles and generates an apk with the merger. 
* The apk is not signed or lined.

-----------------------
es:
* Decompila apk objetivo y apk binder.
* Unifica AndroidManifest.xml de los dos apk's.
* Copia activos y código smali (excepto recursos, ver limitaciones).
* Implementa un receiver que dá de alta en el apk objetivo que actúa de "binder" y que reacciona cuando se conecta el cargador o reinicia el dispositivo.
* Cuando el receiver "despierta", invoca a la clase definida en el properties (que debe de ser un servicio).
* El receiver y el properties son copiados en el "package" objetivo con nombres aleatorios.
* Compila y genera un apk con la fusión realizada.
* El apk no está firmado ni alineado.

Usage
-----
en:
* python ./apk_binder_script.py apk_target.apk apk_bind.apk class.in.apk_bind_to_invoke

If no problems are found the result is stored in "Bind_apk_target.apk"

-----------------------
es:
* python ./apk_binder_script.py apk_target.apk apk_bind.apk class.in.apk_bind_to_invoke

Si no surgen problemas el resultado es almacenado en "Bind_apk_target.apk"

Limitations
-----------
en:
apk_binder_script has certain limitations and works with "bindeados" services. 
Currently no resources or activities to the manifest are copied, and in some cases creates problems recompiling with apktool. 
Viability and use cases for proper implementation etudia. 
When recompiling with apktool certain apks', you may not do it properly generating resource compilation errors, 
but it is a case outside the script. How to decode the file AndroidManifest.xml is studied manually decode avoiding 
all resources.

-----------------------
es:
apk_binder_script tiene ciertas limitaciones y funciona con servicios "bindeados".
Actualmente no se copian recursos ni actividades al manifiesto, ya que en algunos casos genera problemas de recompilación con apktool.
Se etudia la viabilidad y casos de uso para una correcta implementación.
Al recompilar con apktool ciertos apks', es posible que no lo haga correctamente generando errores de compilación de recursos, 
pero es un caso ajeno al script. Se estudia la forma de decodificar el archivo AndroidManifest.xml manualmente evitando así decodificar
todos los recursos.

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
