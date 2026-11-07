#!/usr/bin/env python3
"""Community compatibility patch for the x86_64 Horos 4.0.0 executable."""
import argparse
import hashlib
import os
import plistlib
import shutil
import struct
import subprocess
import sys
from datetime import datetime
from pathlib import Path

CREDIT = 'Desarrollado por Vulmito - ChatGPT y Fran Rielo'
VMADDR = 0x10000EA72
EXPECTED = bytes.fromhex('20 c8 0f b6 c0')
PATCHED = bytes.fromhex('b0 01 0f b6 c0')


def fail(msg):
    raise RuntimeError(msg)


def find_offset(blob):
    # Mach-O 64-bit little endian, thin x86_64 only. Derive mapping from __TEXT segment.
    if len(blob) < 32 or blob[:4] != b'\xcf\xfa\xed\xfe':
        fail('Se requiere un ejecutable Mach-O de 64 bits Intel (x86_64).')
    cpu = struct.unpack_from('<I', blob, 4)[0]
    if cpu != 0x01000007:
        fail('El ejecutable no es x86_64; no se aplicará el parche.')
    ncmds, sizeofcmds = struct.unpack_from('<II', blob, 16)
    pos, end = 32, 32 + sizeofcmds
    if end > len(blob) or ncmds > 10000:
        fail('Cabecera Mach-O incorrecta.')
    for _ in range(ncmds):
        if pos + 8 > end:
            fail('Comandos Mach-O incompletos.')
        cmd, size = struct.unpack_from('<II', blob, pos)
        if size < 8 or pos + size > end:
            fail('Comando Mach-O incorrecto.')
        if cmd == 0x19 and size >= 72:  # LC_SEGMENT_64
            segname = blob[pos + 8:pos + 24].rstrip(b'\0')
            vmaddr, vmsize, fileoff, filesize = struct.unpack_from('<QQQQ', blob, pos + 24)
            if segname == b'__TEXT' and vmaddr <= VMADDR < vmaddr + filesize:
                offset = fileoff + VMADDR - vmaddr
                if offset + len(EXPECTED) <= len(blob):
                    return offset
        pos += size
    fail('No se pudo convertir la dirección de la instrucción a un desplazamiento de archivo.')


def main():
    parser = argparse.ArgumentParser(description='Parche comunitario Horos 4.0.0 (Intel x86_64)')
    parser.add_argument('app', type=Path, help='Ruta de la copia Horos 4.0.0.app')
    parser.add_argument('--apply', action='store_true', help='Aplica el parche (por defecto solo comprueba)')
    parser.add_argument('--no-sign', action='store_true', help='No ejecuta codesign después del parche')
    args = parser.parse_args()
    app = args.app.expanduser().resolve()
    if not app.is_dir() or app.suffix != '.app':
        fail('Indica la ruta de una aplicación .app existente.')
    plist_path = app / 'Contents' / 'Info.plist'
    exe = app / 'Contents' / 'MacOS' / 'Horos'
    if not plist_path.is_file() or not exe.is_file():
        fail('La aplicación no contiene Info.plist y Contents/MacOS/Horos.')
    with plist_path.open('rb') as f:
        info = plistlib.load(f)
    version = info.get('CFBundleShortVersionString')
    if version != '4.0.0':
        fail(f'Versión detectada: {version!r}. Solo se admite Horos 4.0.0.')
    if Path('/Applications/Horos.app').exists() and app.samefile(Path('/Applications/Horos.app')):
        print('AVISO: has seleccionado la aplicación de /Applications; recomendamos parchear una copia.', file=sys.stderr)
    data = exe.read_bytes()
    offset = find_offset(data)
    current = data[offset:offset + len(EXPECTED)]
    print(CREDIT)
    print('Aplicación:', app)
    print('Versión:', version)
    print('SHA-256 actual:', hashlib.sha256(data).hexdigest())
    print('Offset:', hex(offset), 'bytes:', current.hex(' '))
    if current == PATCHED:
        print('El parche ya está aplicado; no se modifica nada.')
        return
    if current != EXPECTED:
        fail('Los bytes no coinciden con la versión compatible. No se ha modificado nada.')
    if not args.apply:
        print('Verificación correcta. Para aplicar, repite con --apply.')
        return
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup = exe.with_name(f'Horos.backup-{timestamp}')
    shutil.copy2(exe, backup)
    new_data = bytearray(data)
    new_data[offset:offset + len(EXPECTED)] = PATCHED
    try:
        with exe.open('r+b') as f:
            f.seek(offset)
            f.write(PATCHED)
            f.flush()
            os.fsync(f.fileno())
        if not args.no_sign:
            # Ad-hoc signature only. Existing developer identity is not preserved.
            subprocess.run(['codesign', '--force', '--deep', '--sign', '-', str(app)], check=True)
    except Exception:
        shutil.copy2(backup, exe)
        print('Error durante la operación: se ha restaurado el ejecutable desde la copia.', file=sys.stderr)
        raise
    print('Parche aplicado correctamente. Backup:', backup)
    print('Nota: la firma original se ha sustituido por una firma ad-hoc.')
    print('Comprueba el funcionamiento con datos de prueba antes de usar estudios clínicos.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, RuntimeError, subprocess.CalledProcessError) as e:
        print('ERROR:', e, file=sys.stderr)
        sys.exit(1)
