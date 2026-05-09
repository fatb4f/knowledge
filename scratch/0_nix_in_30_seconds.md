## 0–Nix in 30 Seconds

- Nix is a **purely functional package manager**: everything is built from recipes (derivations) with no side-effects.
- Every build is **immutable, reproducible, isolated**, pinned by a hash of all inputs.
- Installing something doesn’t mutate your system; Nix creates a new **profile generation** and switches symlinks.
- Multiple versions of anything can coexist because Nix stores everything under `/nix/store/<hash>-name-version`.
- **NixOS** is a full Linux distro built on this idea: your entire system is a declarative configuration.
- **Home Manager** applies the same declarative model to your `$HOME` and user-level configs.
- **Flakes** are structured, reproducible bundles that define inputs, outputs, devShells, and build artifacts.
- Core superpower: **given the same config, you get the same environment on any machine**.
- Typical workflow:
  - Write or reuse a flake
  - Run `nix develop`
  - Instantly enter a fully configured shell with pinned tool versions
- Nix doesn’t replace your workflows; it guarantees the tools exist, exactly as specified, everywhere.