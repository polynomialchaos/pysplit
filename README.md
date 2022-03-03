# pySplit

A Python package for money pool split development.

## Installation

To generate an executable of the **pySplit** package simply call

```sh
pip3 install -e .
```

## Usage

The **pySplit** application either loads an existing case from the specified file (JSON format) or generates a new one if no file is provided.

The user hase the options to

* add exchange rate(s) if the command line option **-e** or **--exchange** is provided, or to

* add member(s) if the command line option **-m** or **--member** is provided, or to

* add purchase(s) if the command line option **-p** or **--purchase** is provided, or to

* add transfer(s) if the command line option **-t** or **--transfer** is provided.

## Output

The **pySplit** stores the defined group information, members, pruchases and transfers in a JSON format file.