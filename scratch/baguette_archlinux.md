Below is a **practical Arch-oriented scaffold** for a Baguette guest. It is not a drop-in guarantee; it is a **starting contract** based on ChromiumOS `vm_tools` and a working Baguette-capable NixOS guest. Core assumptions: ChromeOS provides guest tools via a mounted disk, the guest mounts that disk at `/opt/google/cros-containers`, and the guest starts `maitred`, `vshd`, `port_listener`, and notification forwarding from that mounted toolset. Upstream Baguette is still active and changed again on March 19, 2026, so expect some churn. ([Chromium Git Repositories][1])

## Recommended guest file layout

```text
/etc/systemd/system/
  opt-google-cros\x2dcontainers.mount
  maitred.service
  vshd.service
  cros-port-listener.service
  baguette-first-boot.service

/etc/systemd/user/
  cros-notificationd.service

/etc/dbus-1/services/
  org.freedesktop.Notifications.service

/etc/udev/rules.d/
  99-virtwl.rules

/etc/profile.d/
  10-baguette-envs.sh

/usr/local/libexec/
  baguette-first-boot.sh
```

This layout mirrors the working guest’s main integration points: host tools mount, ChromeOS guest daemons, virtwl permissions, DBus notification activation, and shell environment injection. ([GitHub][2])

## 1. Host tools mount unit

Use the mounted ChromeOS tools disk as the source of truth for guest helper binaries.

**File:** `/etc/systemd/system/opt-google-cros\x2dcontainers.mount`

```ini
[Unit]
Description=ChromeOS guest tools mount
DefaultDependencies=no
Before=local-fs.target multi-user.target
After=systemd-udevd.service
ConditionPathExists=/dev/disk/by-label/cros-vm-tools

[Mount]
What=/dev/disk/by-label/cros-vm-tools
Where=/opt/google/cros-containers
Type=auto
Options=ro,nofail

[Install]
WantedBy=multi-user.target
```

The working Baguette guest mounts `LABEL=cros-vm-tools` read-only at `/opt/google/cros-containers`, and the ChromeOS integration services are launched from that path. ([GitHub][2])

## 2. `maitred` service

**File:** `/etc/systemd/system/maitred.service`

```ini
[Unit]
Description=ChromeOS VM guest agent (maitred)
Requires=opt-google-cros\x2dcontainers.mount
After=opt-google-cros\x2dcontainers.mount dbus.service systemd-udevd.service
ConditionPathExists=/opt/google/cros-containers/bin/maitred

[Service]
Type=simple
ExecStart=/opt/google/cros-containers/bin/maitred
Restart=on-failure
RestartSec=2

[Install]
WantedBy=multi-user.target
```

ChromiumOS documents `maitred` as the VM-side management agent, and the working Baguette guest runs it from the mounted ChromeOS tools disk. ([Chromium Git Repositories][1])

## 3. `vshd` service

**File:** `/etc/systemd/system/vshd.service`

```ini
[Unit]
Description=ChromeOS guest shell daemon (vshd)
Requires=opt-google-cros\x2dcontainers.mount
After=opt-google-cros\x2dcontainers.mount maitred.service
ConditionPathExists=/opt/google/cros-containers/bin/vshd

[Service]
Type=simple
ExecStart=/opt/google/cros-containers/bin/vshd
Restart=on-failure
RestartSec=2

[Install]
WantedBy=multi-user.target
```

`vsh` is part of ChromiumOS `vm_tools`, and the working guest starts `vshd` the same way as the other mounted helpers. ([Chromium Git Repositories][1])

## 4. Port listener service

**File:** `/etc/systemd/system/cros-port-listener.service`

```ini
[Unit]
Description=ChromeOS guest port listener
Requires=opt-google-cros\x2dcontainers.mount
After=opt-google-cros\x2dcontainers.mount maitred.service
ConditionPathExists=/opt/google/cros-containers/bin/port_listener

[Service]
Type=simple
ExecStart=/opt/google/cros-containers/bin/port_listener
Restart=on-failure
RestartSec=2

[Install]
WantedBy=multi-user.target
```

`port_listener` is also part of ChromiumOS `vm_tools`, and the NixOS Baguette example launches it from `/opt/google/cros-containers/bin`. ([Chromium Git Repositories][1])

## 5. Notification forwarding

### User service

**File:** `/etc/systemd/user/cros-notificationd.service`

```ini
[Unit]
Description=ChromeOS notification forwarder
After=default.target
ConditionPathExists=/opt/google/cros-containers/bin/notificationd
ConditionPathExists=/dev/wl0

[Service]
Type=simple
ExecStart=/opt/google/cros-containers/bin/notificationd --virtwl_device=/dev/wl0
Restart=on-failure
RestartSec=2

[Install]
WantedBy=default.target
```

### DBus activation file

**File:** `/etc/dbus-1/services/org.freedesktop.Notifications.service`

```ini
[D-BUS Service]
Name=org.freedesktop.Notifications
Exec=/usr/bin/false
SystemdService=cros-notificationd.service
```

The working guest uses DBus activation for `org.freedesktop.Notifications` and runs notification forwarding against `/dev/wl0`. ([GitHub][2])

## 6. Virtwl udev rule

**File:** `/etc/udev/rules.d/99-virtwl.rules`

```udev
KERNEL=="wl*", MODE="0666"
```

This is the exact permission shape used by the working Baguette guest so `notificationd` can open virtwl devices such as `/dev/wl0`. ([GitHub][2])

## 7. First-boot service

### Script

**File:** `/usr/local/libexec/baguette-first-boot.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

stamp=/var/lib/baguette/first-boot.done
mkdir -p /var/lib/baguette

if [[ -e "$stamp" ]]; then
  exit 0
fi

# Expand the filesystem if the rootfs is Btrfs.
if [[ "$(findmnt -n -o FSTYPE / || true)" == "btrfs" ]]; then
  btrfs filesystem resize max / || true
fi

# Refresh host keys if your image ships prebuilt keys.
ssh-keygen -A || true

# Optional compatibility check: ChromeOS guest startup may expect this path.
if [[ ! -x /usr/sbin/usermod && -x /usr/bin/usermod ]]; then
  mkdir -p /usr/sbin
  ln -sf /usr/bin/usermod /usr/sbin/usermod
fi

touch "$stamp"
```

```bash
chmod +x /usr/local/libexec/baguette-first-boot.sh
```

### Unit

**File:** `/etc/systemd/system/baguette-first-boot.service`

```ini
[Unit]
Description=Baguette guest first-boot tasks
After=local-fs.target
ConditionPathExists=!/var/lib/baguette/first-boot.done

[Service]
Type=oneshot
ExecStart=/usr/local/libexec/baguette-first-boot.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

The working guest resizes Btrfs on activation and ensures compatibility paths expected by `vmc start`; ChromiumOS also recently added first-boot / reboot handling around SSH host keys and shell timing. ([GitHub][2])

## 8. DNS and environment hooks

### DNS

```bash
ln -sf /run/resolv.conf /etc/resolv.conf
```

The working Baguette guest explicitly points resolver handling at `/run/resolv.conf` instead of trying to fully own DNS itself. ([GitHub][2])

### Env hook placeholder

**File:** `/etc/profile.d/10-baguette-envs.sh`

```sh
#!/bin/sh
# Populate this from the current upstream Baguette env script during image build.
# Keep this file close to ChromiumOS's 10-baguette-envs.sh rather than inventing
# a local variant unless you have to.
```

The working guest injects the official Baguette environment logic into shell init rather than reinventing it, and upstream recently fixed timing around providing the user shell only after sommelier-related environment is ready. ([GitHub][2])

## 9. Enable units

```bash
systemctl daemon-reload
systemctl enable opt-google-cros\x2dcontainers.mount
systemctl enable baguette-first-boot.service
systemctl enable maitred.service
systemctl enable vshd.service
systemctl enable cros-port-listener.service
systemctl --global enable cros-notificationd.service
udevadm control --reload
```

## 10. Build/package contract

Use GitHub Actions for deterministic image packaging, not for guest boot validation.

Recommended split:

- GitHub Actions builds the raw image and uploads `baguette_rootfs.img.zst`
- the Chromebook runs `vmc create` / `vmc start` and guest smoke tests
- a self-hosted runner is only needed later if you want boot-time validation in CI

### GitHub Actions boundary

Good fit for hosted runners:

- bootstrap an Arch rootfs
- stage the Baguette integration files from this note
- create a raw disk image
- `mkfs.btrfs` and create `rootfs_subvol`
- copy the rootfs into that subvolume
- compress the result and upload it as an artifact

Bad fit for hosted runners:

- nested VM boot validation
- GUI smoke tests
- anything that depends on actual ChromeOS runtime behavior

Treat that as policy, not as a soft preference. The packaging stage is CI-friendly; the `vmc` runtime stage is not.

### Required build invariants

A packaging script such as `scripts/build-baguette-arch.sh` should own these invariants:

1. produce or import a target-arch Arch rootfs
2. stage the Baguette guest files into that rootfs
3. create a raw image file of a known size
4. run `mkfs.btrfs` on the image
5. attach the image via loop device
6. mount it at a temporary mountpoint
7. create `rootfs_subvol`
8. `rsync` the staged rootfs into `/mnt/rootfs_subvol`
9. set `rootfs_subvol` as the default subvolume
10. unmount, detach loop device, and remove temp dirs
11. compress to `dist/baguette_rootfs.img.zst`

That script should be the only place that knows how to package the image. The workflow file should stay thin and only install host dependencies, call the script, and upload the artifact.

### Failure-safe teardown

This is the operational piece that cannot stay implicit.

The build script should install a `trap` that always attempts:

- `sync`
- `umount` of the mountpoint if mounted
- `losetup -d` of the loop device if attached
- removal of temporary directories

Without that, CI failures leave behind mounted paths or loop devices and the build becomes flaky. This matters locally too, not just in Actions.

### Cross-arch policy

Do not treat "matrix build" as solved unless the rootfs creation path is also solved per architecture.

Packaging an image for `x86_64` and `aarch64` is easy. Producing a valid Arch userspace for both on an Ubuntu GitHub runner is the harder part.

So the safe policy is:

- start with `x86_64`
- only add `aarch64` after you have a defined rootfs bootstrap path for it
- if you add a matrix, make the architecture-specific rootfs creation step explicit rather than assuming the packaging stage is the hard part

### Disk budget assumptions

Hosted runners are tight enough that disk use needs to be explicit.

Budget for all of these at once:

- unpacked/staged rootfs tree
- raw image file
- mounted copy target
- compressed output artifact
- package-manager and tool overhead

That means "lean image" is not just a preference. It is a build constraint. The workflow should avoid retaining extra caches or duplicate trees unless they are justified.

### Workflow contract

The workflow file should stay close to:

```yaml
name: build-baguette-arch

on:
  workflow_dispatch:
  push:
    branches: [main]
    paths:
      - "scripts/**"
      - "baguette/**"
      - ".github/workflows/build-baguette-arch.yml"

jobs:
  build:
    runs-on: ubuntu-24.04

    steps:
      - uses: actions/checkout@v4

      - name: Install host tools
        run: |
          sudo apt-get update
          sudo apt-get install -y btrfs-progs rsync zstd curl xz-utils

      - name: Build image
        run: ./scripts/build-baguette-arch.sh

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: baguette-rootfs-x86_64
          path: dist/baguette_rootfs.img.zst
          if-no-files-found: error
```

Keep the intelligence in the build script, not in the workflow YAML.

## 11. Build-layout checklist

Use this before producing the image:

```text
[ ] Root filesystem is Btrfs
[ ] Default Btrfs subvolume is rootfs_subvol
[ ] Final artifact is a disk image suitable for vmc create --vm-type baguette
[ ] /opt/google/cros-containers exists as mountpoint
[ ] /etc/resolv.conf -> /run/resolv.conf
[ ] systemd units installed for maitred, vshd, port_listener
[ ] user service + DBus activation present for notificationd
[ ] virtwl udev rule installed
[ ] first-boot script installed and enabled
[ ] /usr/sbin/usermod exists or is compat-symlinked
[ ] upstream-style 10-baguette-envs.sh staged into /etc/profile.d
```

Baguette’s documented flow is a purpose-built image format and launch path, not a generic distro VM export, and the upstream smoke tests still revolve around shell access, GUI env, and filesystem growth checks. ([Chromium Git Repositories][1])

## 12. Smoke test after `vmc start`

```bash
systemctl status maitred vshd cros-port-listener
findmnt /opt/google/cros-containers
ls -l /dev/wl0
readlink -f /etc/resolv.conf
df -h /
DISPLAY=:0 glxgears
```

ChromiumOS’s own Baguette docs use GUI and disk-growth smoke tests like `DISPLAY=:0 glxgears` and `df -h` after `vmc start`. ([Chromium Git Repositories][3])

## Notes

* Start with **shell + mount + core services + DNS** first.
* Add **notification forwarding and env polish** second.
* Treat **sommelier/display env** as a timing-sensitive layer, not the first debugging target.
* Do **not** package replacement copies of `maitred`, `vshd`, or `port_listener`; mount and use the host-provided ChromeOS guest tools instead. ([Chromium Git Repositories][1])

I can turn this into a **single Arch package/install script bundle** next: `PKGBUILD`, unit files, and a `justfile` target to stage everything into a rootfs tree.

[1]: https://chromium.googlesource.com/chromiumos/platform2/%2B/main/vm_tools?utm_source=chatgpt.com "vm_tools - chromiumos/platform2 - Git at Google"
[2]: https://github.com/aldur/nixos-crostini/blob/main/baguette.nix?utm_source=chatgpt.com "nixos-crostini/baguette.nix at main"
[3]: https://chromium.googlesource.com/chromiumos/platform2/%2B/23a9cab4008d51491c5976863929164a12af07bc?utm_source=chatgpt.com "23a9cab4008d51491c59768639..."

## Appendix. MARASOV submarine-first checklist

For `MARASOV`, prefer a `Submarine` test path before any firmware replacement path.
The practical reason is simple: `Submarine` can be booted from USB while retaining
stock ChromeOS firmware, which makes bring-up much safer than `UEFI Full ROM`.

### Decision rule

- Prefer `Submarine` first.
- Do not treat `MrChromebox UEFI Full ROM` as the default path for `MARASOV`.
- Only consider internal-disk `Submarine` after USB boot proves the device is usable.

### Why this path

- `Submarine` can be written to USB as a bootable image and tested with `Ctrl+U`.
- This keeps the stock firmware path intact while evaluating Linux behavior.
- `MARASOV` has enough public boot/audio rough-edge history on the UEFI path that a
  firmware-replacement-first approach is not the low-risk option.

### USB-first test flow

1. Obtain or build the `x86_64` `submarine.bin` image.
2. Write it to removable media:

```bash
sudo dd if=build/submarine.bin of=/dev/sdX bs=4M status=progress oflag=sync
```

3. Boot the Chromebook to the developer-mode screen.
4. Insert the drive.
5. Press `Ctrl+U`.
6. Confirm that the submarine boot menu appears.

### First-pass validation targets

Only answer these questions on the first pass:

1. Does submarine boot reliably from USB?
2. Is the internal storage visible at all?
3. Do keyboard and touchpad work?
4. Does Wi-Fi come up?
5. Does suspend/resume work?
6. Does internal speaker audio work without obvious distortion?

If any one of storage, suspend, or audio is broken, do not move to an internal-disk
install yet.

### MARASOV-specific caution

The most relevant submarine-specific risk to watch is internal storage visibility,
especially if the unit uses `UFS`. Treat that as the main blocker check on first boot.

### Promotion rule

Promote from USB test to internal install only if all of the following are true:

- submarine boots reliably from USB
- internal storage is detected
- keyboard/touchpad are usable
- Wi-Fi is usable
- suspend/resume is acceptable
- internal audio is acceptable

### Internal install only after USB success

If the USB test passes, then consider creating a small boot partition for submarine
and writing the `.kpart` image there. Do not start with that path.
