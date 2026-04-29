# Thermalright LCD Control CLI

Linux CLI/service control for Thermalright LCD coolers and USB displays.

This is an unofficial reverse-engineered project. It is not Thermalright code, and it should be treated as a hardware-control hack: review it, run it in an isolated VM if possible, and expect some device-specific trial and error.

## What It Does

This tool detects a supported Thermalright LCD device, writes a device config, and runs a background service that continuously sends rendered frames to the display.

It is intentionally CLI-only. The original GUI code has been removed.

Supported display content includes:

- CPU usage, frequency, and temperature where Linux exposes the sensor data.
- GPU usage, frequency, name, vendor, and temperature where the GPU is visible to the OS.
- RAM usage.
- Time/date text.
- Static images, GIFs, videos, and image collections as backgrounds.
- Foreground overlays and YAML-configured text positioning.

## Supported Devices

| VID:PID | Resolution | Transport |
| --- | ---: | --- |
| `0416:5302` | `320x240` | HID |
| `0416:8001` | `480x480` | HID |
| `0418:5304` | `480x480` | HID |
| `87AD:70DB` | `320x320` or `480x480` | USB |

For your device, `0416:8001`, the tool uses the `480x480` profile and loads:

```text
~/.config/thermalright-lcd-control/config/config_480480.yaml
```

## VM And Proxmox Notes

If this runs inside a VM, the metrics are from the VM's point of view.

Example: if the VM has 4 vCPU and 8 GB RAM, the LCD shows usage for those 4 vCPU and 8 GB RAM, not the full Proxmox host.

To show real Proxmox host metrics while keeping USB control inside a VM, expose host metrics to the VM over the network, for example with Prometheus node exporter, SSH polling, or a small HTTP endpoint.

Running directly on the Proxmox host can work, but it is riskier because this service runs with USB/HID access. A VM with USB passthrough is the safer setup.

## Install In A VM

First pass the LCD USB device through to the VM from Proxmox.

On the Proxmox host:

```bash
lsusb
```

Look for:

```text
0416:8001
```

In the Proxmox UI:

```text
VM -> Hardware -> Add -> USB Device -> select 0416:8001
```

Then fully restart the VM and confirm the device is visible inside it:

```bash
lsusb | grep 0416
```

Install system dependencies inside the VM:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip curl libusb-1.0-0
```

Install `uv` if it is not already installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
uv --version
```

Extract or clone this repo, then run:

```bash
sudo ./install.sh
```

The installer copies app files, creates a Python virtual environment, installs the CLI launcher, copies configs/themes, detects the USB device, writes `device_info.yaml`, and installs the systemd service.

For a root-only VM/container, direct root execution is supported:

```bash
./install.sh
```

You can force a specific target user during direct root install:

```bash
INSTALL_USER=myuser ./install.sh
```

## Run

Start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now thermalright-lcd-control
```

Check status:

```bash
sudo systemctl status thermalright-lcd-control
```

Follow logs:

```bash
sudo journalctl -u thermalright-lcd-control -f
```

Run the CLI manually:

```bash
thermalright-lcd-control
```

## Configuration

Installed configs live here:

```text
~/.config/thermalright-lcd-control/config/
```

For `0416:8001`, edit:

```text
~/.config/thermalright-lcd-control/config/config_480480.yaml
```

The service watches the config file timestamp and reloads display generation when the config changes.

Metric entries look like this:

```yaml
- color: '#FFFFFFFF'
  enabled: true
  font_size: 24
  format_string: '{label}{value:.0f}{unit}'
  label: 'RAM '
  name: ram_usage
  position:
    x: 195
    y: 290
  unit: '%'
```

Available metric names currently include:

- `cpu_temperature`
- `cpu_usage`
- `cpu_frequency`
- `cpu_name`
- `gpu_temperature`
- `gpu_usage`
- `gpu_frequency`
- `gpu_vendor`
- `gpu_name`
- `ram_usage`

Temperature and GPU metrics depend on what the VM or Linux host can actually see. In a VM, CPU temperatures are commonly unavailable unless explicitly exposed.

## Package Build

If you want to create a release archive:

```bash
./create_package.sh
```

That script expects `uv` to be installed.

## Uninstall

```bash
sudo ./uninstall.sh
```

## Troubleshooting

If no device is detected, confirm USB passthrough first:

```bash
lsusb
```

If permissions fail, run the service as installed through systemd rather than as an unprivileged shell user.

If the display resolution is wrong, remove the generated device info and rerun the installer/device init:

```bash
rm ~/.config/thermalright-lcd-control/config/device_info.yaml
sudo ./install.sh
```

If the service starts but the screen does not update, inspect logs:

```bash
sudo journalctl -u thermalright-lcd-control -n 200 --no-pager
```

## License

Apache-2.0. See `LICENSE`.
