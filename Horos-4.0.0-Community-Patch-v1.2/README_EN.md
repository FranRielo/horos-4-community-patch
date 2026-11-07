# Horos 4.0.0 Community Patch v1.2

**Developed by Vulmito - ChatGPT and Fran Rielo**

Experimental compatibility patch for a specific **Horos 4.0.0 Intel x86_64** build that incorrectly reports “This application requires macOS 10.11 or higher” on newer macOS versions.

## Double-click installation

1. Download and extract the ZIP on your Mac.
2. Double-click **INSTALAR - doble clic.command**. If macOS blocks the launcher, review its source and allow it through the system's security controls only if you trust the package. Do not disable Gatekeeper globally.
3. Select your **original, unpatched Horos 4.0.0** application (possibly `/Applications/Horos.app`).
4. Read the warning and enter `s` followed by Return to confirm.
5. The launcher **never modifies the original application**. It creates a new Desktop copy (`Horos-4.0.0-Comunidad-Parcheado.app`), removes extended attributes **from that copy only**, patches the executable, and applies an ad-hoc signature.
6. Open the newly created copy and test it.

If the destination exists, a numbered name is used without overwriting. No `sudo` required. Requires Python 3 and standard macOS tools (`ditto`, `xattr`, `codesign`, `osascript`).

## Technical details

In `+[AppController hasMacOSXElCapitan]`, replaces the 5-byte sequence `20 c8 0f b6 c0` with `b0 01 0f b6 c0`. The Python script checks the app version, architecture and bytes before modifying it.

## Safety and limitations

- The launcher runs `xattr -cr` on the **new copy only**, also removing its quarantine marker. Use only trusted Horos binaries.
- The original developer signature is replaced with an **ad-hoc** signature; this is neither Apple notarization nor a Developer ID signature.
- Unofficial community patch, not universally tested across macOS versions or Horos features.
- Tested manually on one Mac with an independent installation. **Not clinically validated.** Test with nonclinical data and follow institutional requirements before any clinical use.
- The original Horos application, Horos 3.3.5 and other installations are not changed. The patched copy contains a backup executable.
- If patching fails, the new copy may be incomplete; the original remains untouched.

## Advanced command-line usage

```bash
python3 patch_horos.py "/path/Horos.app"           # Verify only
python3 patch_horos.py --apply "/path/Horos.app"   # Modifies that app directly
```

The advanced method modifies the selected path and may fail due to permissions or extended attributes; prefer the double-click launcher.

MIT license. Credit: **Desarrollado por Vulmito - ChatGPT y Fran Rielo**.
