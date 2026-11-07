#!/bin/bash
# Horos 4.0.0 Community Patch v1.2
# Desarrollado por Vulmito - ChatGPT y Fran Rielo
set -euo pipefail
cd "$(dirname "$0")"
printf '\n============================================\n'
printf ' HOROS 4.0.0 - COMMUNITY PATCH v1.2\n'
printf ' Desarrollado por Vulmito - ChatGPT y Fran Rielo\n'
printf '============================================\n\n'
finish() {
  status=$?
  if [ "$status" -ne 0 ]; then
    printf '\nERROR: no se ha completado la operación (código %s).\n' "$status"
    printf 'La aplicación original no se ha modificado.\n'
  fi
  printf '\nPulsa Intro para cerrar esta ventana... '
  read -r _ || true
}
trap finish EXIT

if ! command -v python3 >/dev/null 2>&1; then
  echo 'ERROR: Python 3 no está instalado o no está disponible en PATH.'
  echo 'Instala Python 3 o las herramientas de desarrollo de Apple y vuelve a probar.'
  exit 1
fi

if ! command -v osascript >/dev/null 2>&1; then
  echo 'ERROR: AppleScript no disponible.'
  exit 1
fi

printf 'Selecciona la aplicación ORIGINAL Horos 4.0.0 en el cuadro de diálogo.\n'
printf 'No selecciones Horos 3.3.5 ni otra copia ya parcheada.\n\n'
if ! selected=$(osascript -e 'try' -e 'set chosen to choose file with prompt "Selecciona Horos 4.0.0.app ORIGINAL (sin parchear)" of type {"app"}' -e 'return POSIX path of chosen' -e 'on error number -128' -e 'return ""' -e 'end try'); then
  echo 'No se ha podido mostrar el selector de archivos.'
  exit 1
fi
if [ -z "$selected" ]; then
  echo 'Operación cancelada.'
  exit 0
fi
# AppleScript devuelve los paquetes .app como directorios y suele añadir una barra final.
# Normalizamos la ruta antes de comprobar la extensión.
selected="${selected%/}"
if [ ! -d "$selected" ] || [[ "$selected" != *.app ]]; then
  echo 'ERROR: debes seleccionar una aplicación .app.'
  exit 1
fi

# Check original BEFORE copying, without modifying it.
echo 'Comprobando la aplicación original (solo lectura)...'
python3 ./patch_horos.py "$selected"

base="$HOME/Desktop/Horos-4.0.0-Comunidad-Parcheado.app"
dest="$base"
i=2
while [ -e "$dest" ]; do
  dest="$HOME/Desktop/Horos-4.0.0-Comunidad-Parcheado-$i.app"
  i=$((i+1))
done

printf '\nOrigen: %s\n' "$selected"
printf 'Nueva copia: %s\n' "$dest"
printf 'El original NO se modificará.\n'
printf 'La copia perderá su firma original y los atributos extendidos, incluida la cuarentena.\n'
printf 'Continúa solo si confías en el origen de esta aplicación.\n\n'
read -r -p '¿Crear la copia y parchearla? [s/N]: ' reply
case "$reply" in
  s|S|si|SI|Si|sí|Sí) ;;
  *) echo 'Cancelado sin cambios.'; exit 0 ;;
esac

printf '\nCopiando aplicación (puede tardar unos minutos)...\n'
ditto "$selected" "$dest"

# Clean only the fresh copy; codesign rejects resource forks and Finder metadata.
printf 'Limpiando atributos extendidos únicamente en la copia...\n'
xattr -cr "$dest"

printf '\nAplicando parche y firma ad-hoc...\n'
python3 ./patch_horos.py --apply "$dest"

printf '\nVerificando la firma...\n'
codesign --verify --deep --verbose=2 "$dest"
printf '\n¡ÉXITO! Aplicación parcheada en:\n%s\n' "$dest"
printf '\nAbre esta copia desde el Escritorio para comprobarla.\n'
printf 'Prueba con estudios DICOM no clínicos antes de cualquier uso asistencial.\n'
