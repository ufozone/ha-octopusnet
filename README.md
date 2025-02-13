# Digital Devices Octopus NET Monitoring

[![License][license-shield]](LICENSE)
![Project Maintenance][maintenance-shield]
[![GitHub Activity][commits-shield]][commits]

[![hacs][hacsbadge]][hacs]
[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

[![GitHub Release][release-shield]][releases]
[![issues][issues-shield]][issues-link]
[![release-badge]][release-workflow]
[![validate-badge]][validate-workflow]
[![lint-badge]][lint-workflow]

Digital Devices Octopus NET Monitoring as a Custom Component for Home Assistant. Octopus NET with firmware `octonet-pro-2.0.0` or higher are supported.

## Installation

> [!IMPORTANT]
> Requires Home Assistant 2025.2.0 or newer.

### Installation through HACS

Installation using Home Assistant Community Store (HACS) is recommended.

1. If HACS is not installed, follow HACS installation and configuration at <https://hacs.xyz/>.

2. Click the button below or visit HACS and add `https://github.com/ufozone/ha-octopusnet.git` as a custom repository with type `Integration` by following [these instructions](https://hacs.xyz/docs/faq/custom_repositories/).

    [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ufozone&repository=ha-octopusnet&category=integration)

3. Install the integration.

4. Restart Home Assistant!

5. Make sure that you refresh your browser window too.

### Manual installation

1. Download the `octopusnet.zip` file from the repository [release section](https://github.com/ufozone/ha-octopusnet/releases).

   Do **not** download directly from the `main` branch.

2. Extract and copy the content into the path `/config/custom_components/octopusnet` of your HA installation.

3. Restart Home Assistant!

4. Make sure that you refresh your browser window too.

### Setup integration

Start setup:

* Click this button:

    [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=octopusnet)

* Or use the "Add Integration" in Home Assistant, Settings, Devices & Services and select "Digital Devices Octopus NET Monitoring".

## Configuration

* All configuration options are offered from the front end.

## Available components

### Binary Sensors

* binary_sensor.*{host}*_epg

  Attributes:

  ```text
  total, events, last_poll
  ```

* binary_sensor.*{host}*\_tuner_*{n}*

  *This entity is disabled by default. You have to activate it if you want to use it.*

  Attributes:

  ```text
  lock, strength, snr, quality, level, last_poll
  ```

* binary_sensor.*{host}*\_stream_*{n}*

  *This entity is disabled by default. You have to activate it if you want to use it.*

  Attributes:

  ```text
  input, packets, bytes, client, last_poll
  ```

### Buttons

* button.*{host}*_update

  Attributes:

  ```text
  last_poll
  ```

* button.*{host}*_reboot

  Attributes:

  ```text
  last_poll
  ```

* button.*{host}*_epg_scan

  Attributes:

  ```text
  last_poll
  ```

### Sensors

* sensor.*{host}*_fanspeed

  Attributes:

  ```text
  last_poll
  ```

* sensor.*{host}*_temperature

  Attributes:

  ```text
  last_poll
  ```

* sensor.*{host}*_tuner

  Attributes:

  ```text
  count, avg. strength, avg. snr, avg. quality, avg. level, last_poll
  ```

* sensor.*{host}*_stream

  Attributes:

  ```text
  total input, total packets, total bytes, total clients, last_poll
  ```

### Services

* `octopusnet.epg_scan`

    Start the EPG scan.

* `octopusnet.reboot`

    Reboot the device.

### Logging

Set the logging to debug with the following settings in case of problems.

```yaml
logger:
  default: warn
  logs:
    custom_components.octopusnet: debug
```

***

[commits-shield]: https://img.shields.io/github/commit-activity/y/ufozone/ha-octopusnet?style=for-the-badge
[commits]: https://github.com/ufozone/ha-octopusnet/commits/main
[license-shield]: https://img.shields.io/github/license/ufozone/ha-octopusnet.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-ufozone-blue.svg?style=for-the-badge

[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/

[releases]: https://github.com/ufozone/ha-octopusnet/releases
[release-shield]: https://img.shields.io/github/v/release/ufozone/ha-octopusnet?style=flat

[issues-shield]: https://img.shields.io/github/issues/ufozone/ha-octopusnet?style=flat
[issues-link]: https://github.com/ufozone/ha-octopusnet/issues

[lint-badge]: https://github.com/ufozone/ha-octopusnet/actions/workflows/lint.yaml/badge.svg
[lint-workflow]: https://github.com/ufozone/ha-octopusnet/actions/workflows/lint.yaml
[validate-badge]: https://github.com/ufozone/ha-octopusnet/actions/workflows/validate.yaml/badge.svg
[validate-workflow]: https://github.com/ufozone/ha-octopusnet/actions/workflows/validate.yaml
[release-badge]: https://github.com/ufozone/ha-octopusnet/actions/workflows/release.yaml/badge.svg
[release-workflow]: https://github.com/ufozone/ha-octopusnet/actions/workflows/release.yaml
