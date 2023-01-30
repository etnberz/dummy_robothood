# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[comment]: <> (towncrier release notes start)

## [0.7.0] 2023-01-24
### Fixed
- Fix database creation permission with Docker
[MR11](https://github.com/etnberz/robothood/pull/11)
- Fix target reached message management by the bot
[MR16](https://github.com/etnberz/robothood/pull/16)
- Fix discum by changing its version.
[MR19](https://github.com/etnberz/robothood/pull/19)
- Fix OCO sell order bug: they were not executed.
[MR23](https://github.com/etnberz/robothood/pull/23)
- Change prices conversion process
[MR24](https://github.com/etnberz/robothood/pull/24)
- Fix sell price conversion
[MR25](https://github.com/etnberz/robothood/pull/25)

### Added
- Add the signal storage feature in a SQL DB, signals are stored and their status updated dynamically.
[MR8](https://github.com/etnberz/robothood/pull/8)
- Add `leftovers.py` to manage orders that has not been executed yet
[MR11](https://github.com/etnberz/robothood/pull/11)
- Add real currency conversion functions.
[MR12](https://github.com/etnberz/robothood/pull/12)
- Add USDT as base currency.
[MR22](https://github.com/etnberz/robothood/pull/22)
- Sell at multiple target prices
[MR25](https://github.com/etnberz/robothood/pull/25)

### Changed
- Make ROBOTHOOD_PATH env var mandatory again
[MR10](https://github.com/etnberz/robothood/pull/10)
- Release v0.5.0
[MR14](https://github.com/etnberz/robothood/pull/14)
- Change the discord message format.
[MR18](https://github.com/etnberz/robothood/pull/18)
- Change discum version
[MR20](https://github.com/etnberz/robothood/pull/20)
- Change discum for discord.py-self
[MR21](https://github.com/etnberz/robothood/pull/21)
- Change all the objects to accept other base currency than BTC.
[MR22](https://github.com/etnberz/robothood/pull/22)
- Enable having a custom selling strategy using a weight for each target.
[MR26](https://github.com/etnberz/robothood/pull/26)
- Rename the entire project for robothood.
[MR29](https://github.com/etnberz/robothood/pull/29)
- Change the readme style and content.
[MR30](https://github.com/etnberz/robothood/pull/30)

### Internals
- Change tests to be independent from binance env variables and add a PR template
[MR9](https://github.com/etnberz/robothood/pull/9)
- Remove no env var decorator on tests
[MR13](https://github.com/etnberz/robothood/pull/13)
- Refactor tests: mocking the binance client itself and re organize tests.
[MR27](https://github.com/etnberz/robothood/pull/27)
- Add a docker build in the Github Actions CI.
[MR28](https://github.com/etnberz/robothood/pull/28)


## [0.5.0] 2022-05-03
### Fixed
- Fix database creation permission with Docker
[MR11](https://github.com/etnberz/robothood/pull/11)

### Added
- Add the signal storage feature in a SQL DB, signals are stored and their status updated dynamically.
[MR8](https://github.com/etnberz/robothood/pull/8)
- Add `leftovers.py` to manage orders that has not been executed yet
[MR11](https://github.com/etnberz/robothood/pull/11)
- Add real currency conversion functions.
[MR12](https://github.com/etnberz/robothood/pull/12)

### Changed
- Make ROBOTHOOD_PATH env var mandatory again
[MR10](https://github.com/etnberz/robothood/pull/10)
- Release v0.5.0
[MR14](https://github.com/etnberz/robothood/pull/14)

### Internals
- Change tests to be independent from binance env variables and add a PR template
[MR9](https://github.com/etnberz/robothood/pull/9)
- Remove no env var decorator on tests
[MR13](https://github.com/etnberz/robothood/pull/13)


## [0.4.0] 2022-03-04
### Fixed
- Fix the logs in file with a docker run.
[MR5](https://github.com/etnberz/robothood/pull/5)

### Added
- Add a `entrypoint.sh` file as an entrypoint for the DockerImage and a `run.sh` file to run docker.
[MR5](https://github.com/etnberz/robothood/pull/5)
- Add Github Actions CI
[MR6](https://github.com/etnberz/robothood/pull/6)


## [0.3.0] 2022-02-23
### Added
- Enable docker running for the bot and write the associated documentation in readme.
[MR2](https://github.com/etnberz/robothood/pull/2)

### Changed
- Changed towncrier link and path management for logging in robothood init.
[MR2](https://github.com/etnberz/robothood/pull/2)

## [0.2.0] 2022-02-23
Fail Bumpversion

## [0.1.0] 2022-02-02
- Initial Project Creation, first working POC.
[MR1](https://github.com/etnberz/robothood/pull/1)
