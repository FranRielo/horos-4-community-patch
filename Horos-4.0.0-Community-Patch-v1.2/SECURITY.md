# Security / Seguridad

This unofficial project modifies executable bytes and replaces the application's code signature with an ad-hoc signature. The launcher also removes extended attributes, **including macOS quarantine**, from the *newly copied* application. These operations reduce some macOS provenance checks; use only a Horos build obtained from a trusted source. Do not disable Gatekeeper system-wide.

The script performs version, architecture and instruction-byte checks but **does not authenticate the original application**. A matching byte sequence is not proof of a trustworthy download. It does not ship Horos.

For security concerns, avoid posting patient data or secrets in public issues. Contact the repository maintainer through a private channel once one is provided.
