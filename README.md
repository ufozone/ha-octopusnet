# Digital Devices Octopus NET Monitoring
[![License][license-shield]](LICENSE)
![Project Maintenance][maintenance-shield]
[![GitHub Activity][commits-shield]][commits]

[![hacs][hacsbadge]][hacs]
[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

Stable -
[![GitHub Release][stable-release-shield]][releases]
[![release-badge]][release-workflow]

Latest -
[![GitHub Release][latest-release-shield]][releases]
[![validate-badge]][validate-workflow]
[![lint-badge]][lint-workflow]
[![issues][issues-shield]][issues-link]

> :warning: **This integration is in development.**

Digital Devices Octopus NET Monitoring as a Custom Component for Home Assistant. Octopus NET with firmware `octonet-pro-2.0.0` or higher are supported.

## Installation
* First: This is not a Home Assistant Add-On. It's a custom component.
* There are two ways to install. First you can download the folder custom_component and copy it into your Home-Assistant config folder. Second option is to install HACS (Home Assistant Custom Component Store) and select "Digital Devices Octopus NET Monitoring" from the Integrations catalog.
* Restart Home Assistant after installation
* Make sure that you refresh your browser window too
* Use the "Add Integration" in Home Assistant, Settings, Devices & Services and select "Digital Devices Octopus NET Monitoring"

## Available components 

### Binary Sensors

t.b.a

### Sensors

t.b.a

### Services

* epg_scan

* reboot

### Logging

Set the logging to debug with the following settings in case of problems.

```
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

[issues-shield]: https://img.shields.io/github/issues/ufozone/ha-octopusnet?style=flat
[issues-link]: https://github.com/ufozone/ha-octopusnet/issues

[releases]: https://github.com/ufozone/ha-octopusnet/releases
[stable-release-shield]: https://img.shields.io/github/v/release/ufozone/ha-octopusnet?style=flat
[latest-release-shield]: https://img.shields.io/github/v/release/ufozone/ha-octopusnet?include_prereleases&style=flat

[lint-badge]: https://github.com/ufozone/ha-octopusnet/actions/workflows/lint.yaml/badge.svg
[lint-workflow]: https://github.com/ufozone/ha-octopusnet/actions/workflows/lint.yaml
[validate-badge]: https://github.com/ufozone/ha-octopusnet/actions/workflows/validate.yaml/badge.svg
[validate-workflow]: https://github.com/ufozone/ha-octopusnet/actions/workflows/validate.yaml
[release-badge]: https://github.com/ufozone/ha-octopusnet/actions/workflows/release.yaml/badge.svg
[release-workflow]: https://github.com/ufozone/ha-octopusnet/actions/workflows/release.yaml
