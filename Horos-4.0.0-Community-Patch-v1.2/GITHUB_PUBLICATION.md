# GitHub publication checklist / Publicación

1. Sign in to GitHub and create a **public repository** named `horos-4-community-patch` (or choose another name). Do **not** initialize it with a README/license because those are included.
2. Unzip this package, open Terminal in its folder, then run:

   ```bash
   git init
   git add .
   git commit -m "Release Horos 4.0.0 Community Patch v1.2"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/horos-4-community-patch.git
   git push -u origin main
   ```

   Replace `YOUR_USERNAME` with your GitHub username. GitHub may ask you to authenticate. The ZIP is a source distribution; no Horos executable is included.
3. On GitHub, select **Releases → Draft a new release**, tag `v1.2.0`, title `Horos 4.0.0 Community Patch v1.2`, and paste `RELEASE_NOTES.md`.
4. Attach the ZIP to the release. Clearly mark it **experimental / unofficial / not clinically validated**.
5. Before promoting broadly, test on at least one additional Intel Mac and verify with nonclinical DICOM samples.

Do not claim that GitHub publication or additional compatibility testing has already occurred.
