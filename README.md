# Horos 4.0.0 Community Patch v1.2

**Desarrollado por Vulmito - ChatGPT y Fran Rielo**

[Español](README_ES.md) · [English](README_EN.md) · [Notas de versión](RELEASE_NOTES.md)

Experimental, **unofficial** compatibility patch for a specific **Intel x86_64 Horos 4.0.0** build showing the incorrect message “This application requires macOS 10.11 or higher” on newer macOS versions.

## Quick start / Inicio rápido

1. Obtain Horos 4.0.0 from a trusted source; **Horos itself is not included**.
2. Download the source ZIP from the GitHub release, extract it, and double-click `INSTALAR - doble clic.command` on macOS.
3. Select the **unmodified** Horos 4.0.0 `.app`; confirm the operation in Terminal.
4. A separately patched copy is created on the Desktop. The original remains untouched.

Requires macOS with Python 3 and standard Apple command-line utilities (`osascript`, `ditto`, `xattr`, `codesign`). The launcher clears extended attributes, **including quarantine**, only on the new copy, and replaces its signature with an **ad-hoc signature**. Do not run on untrusted software. Do not disable Gatekeeper globally.

**Status:** manually reported successful on one Mac; not tested across Mac models, macOS releases, or clinical workflows. **Not validated for clinical use.** Use nonclinical test data and comply with local institutional requirements.

MIT license applies to this patch's source code, not to Horos itself. Not affiliated with or endorsed by the Horos project.
