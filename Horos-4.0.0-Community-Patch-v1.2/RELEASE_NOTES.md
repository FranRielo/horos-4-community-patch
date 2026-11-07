# v1.2 — GitHub community release candidate

- Bundles the double-click launcher and Python patcher previously tested as v1.1.1.
- Keeps source Horos installation untouched; creates a separately named Desktop copy.
- Normalizes trailing slash returned by the macOS file chooser.
- Verifies version 4.0.0, Intel x86_64 Mach-O format and exact original instruction bytes before patching.
- Creates executable backup, re-signs the copy ad-hoc and verifies signature.
- Documents extended-attribute cleanup and its security implications.
- Adds bilingual usage instructions, GitHub issue templates, contribution guidance, release checklist and CI syntax checks.
- Minor readability change in the Python warning for `/Applications/Horos.app`.

**Known limitations:** tested manually on only one Mac; Intel x86_64 build only; no official Horos endorsement; not validated for clinical use; Python 3 required; ad-hoc signature replaces developer signature; quarantine removed on the new copy; original app must match the exact expected bytes. No claim of compatibility with all macOS releases.
