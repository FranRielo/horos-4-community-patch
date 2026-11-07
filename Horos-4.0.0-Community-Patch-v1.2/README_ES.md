# Horos 4.0.0 Community Patch v1.2

**Desarrollado por Vulmito - ChatGPT y Fran Rielo**

Parche experimental de compatibilidad para una compilación concreta de **Horos 4.0.0 Intel x86_64** que muestra incorrectamente «This application requires macOS 10.11 or higher» en versiones recientes de macOS.

## Instalación (doble clic)

1. Descarga y descomprime el ZIP en el Mac.
2. Abre **INSTALAR - doble clic.command** (doble clic). Si macOS bloquea el lanzador, revisa su procedencia y autorízalo desde los controles de seguridad del sistema solo si confías en este paquete. No desactives Gatekeeper globalmente.
3. En el selector, elige la aplicación **Horos 4.0.0 original, sin parchear**. Puede estar en `/Applications/Horos.app`.
4. Lee el aviso y confirma escribiendo `s` seguido de Intro.
5. El instalador **no modifica el Horos original**: crea una copia independiente en el Escritorio (`Horos-4.0.0-Comunidad-Parcheado.app`), elimina los atributos extendidos de **esa copia** y aplica el parche y una firma ad-hoc.
6. Abre la nueva copia y comprueba su funcionamiento.

Si ya existe una copia con ese nombre, el instalador genera un nombre nuevo sin sobrescribirla. No se necesita `sudo`. Se requiere **Python 3**, `ditto`, `xattr`, `codesign` y `osascript` en macOS.

## Qué corrige

En el método `+[AppController hasMacOSXElCapitan]`, reemplaza los 5 bytes `20 c8 0f b6 c0` por `b0 01 0f b6 c0` en la dirección correspondiente. Verifica la versión, arquitectura y bytes antes de actuar. La detección original de versión falla en ciertos macOS modernos.

## Seguridad y limitaciones

- El lanzador usa `xattr -cr` **solo en la copia creada**, lo que también elimina la marca de cuarentena de dicha copia. Utiliza únicamente aplicaciones de origen confiable.
- La firma original del desarrollador se sustituye por una **firma ad-hoc**; no equivale a una firma de desarrollador ni a una notarización de Apple.
- No es un parche oficial de Horos ni garantiza compatibilidad universal con macOS o todas las funciones.
- Se ha probado manualmente en un equipo y una instalación independiente. **No es una validación clínica.** Comprueba el funcionamiento con datos no clínicos y sigue los requisitos de tu centro antes de cualquier uso asistencial.
- No modifica Horos 3.3.5 ni otros programas. El script crea un respaldo del ejecutable dentro de la nueva copia.
- Si falla el proceso, la copia puede quedar incompleta; el original permanece intacto. Borra la copia fallida si es necesario.

## Uso avanzado

```bash
python3 patch_horos.py "/ruta/Horos.app"           # Comprobar
python3 patch_horos.py --apply "/ruta/Horos.app"   # Modificar esa ruta directamente
```

El método avanzado **sí modifica la ruta elegida** y puede fallar por permisos o atributos extendidos; se recomienda el lanzador de doble clic.

## Licencia

MIT. Consulta `LICENSE`. Créditos: **Desarrollado por Vulmito - ChatGPT y Fran Rielo**.
