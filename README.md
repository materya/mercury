<h1 align="center">
  <img src="doc/assets/mercury_materya_logo.png" alt="Mercury Materya" />
</h1>

[![License][license-image]][license-url]

A quantitative trading library.

[Mercury](https://en.wikipedia.org/wiki/Mercury_(mythology)) is a major god in Roman mythology.  
He is, among other things, the god of financial gain and communication (including divination).  

## Quick start

### Install

#### With pip

```shell
$ pip install materya-mercury
```

#### From source

Clone this repo and run

```shell
$ make
```

#### Extras Dependencies

The library provides some [extras modules](#extras-modules) implementing interfaces of `mercury` as examples and helpers to quickly setup your own strategies.

You can install their eventual dependencies with

```shell
$ pip install materya-mercury[extra_<type>_<module name>]
```

e.g. to install extras dependencies for alphavantage datasource

```shell
$ pip install materya-mercury[extra_datasource_alphavantage]
```

### Usage

Coming soon

See [Samples](samples)

### Extras Modules

#### Brokers

- Interactive Brokers
- Oanda
- XAPI

#### Datasources

- Alphavantage
- CSV
- Quandl

#### Strategies

- SMA Crossover

## Contributing

### Development

A fully configured [VSCode Development Container](https://code.visualstudio.com/docs/remote/containers) is available to quickly get into development without the hassle of setting up a local environment, you just have to jump in.

Alternatively you can use a development container without VS Code, the setup is available with `docker-compose` to inspect or run tests against the library in a compatible environment.

```shell
$ docker-compose run --rm dev bash
Creating mercury_dev_run ... done

cloud@8e5fb622c5c5:/workspace$ make test
```

If you prefer to work locally (or don't use VSCode), you need first to install the library in a development mode:

```shell
$ make install-dev
```

### Test

You can simply run the test suite in the current environment with:

  ```shell
  $ make test
  ```

## License

[GPL-3.0](LICENSE)

[license-image]: https://img.shields.io/github/license/materya/mercury?style=flat-square
[license-url]: LICENSE
