<p align="center">
<img src="horizontal-logo.png" height="150">
</p>

<h1 align="center">
  ContNeXtViewer
</h1>

<p align="center">
    <a href="https://github.com/ContNeXt/web_app/actions?query=workflow%3ATests">
        <img alt="Tests" src="https://github.com/ContNeXt/web_app/workflows/Tests/badge.svg" />
    </a>
    <a href="https://github.com/cthoyt/cookiecutter-python-package">
        <img alt="Cookiecutter template from @cthoyt" src="https://img.shields.io/badge/Cookiecutter-python--package-yellow" /> 
    </a>
    <a href="https://pypi.org/project/contnextViewer">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/contnextViewer" />
    </a>
    <a href="https://pypi.org/project/contnextViewer">
        <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/contnextViewer" />
    </a>
    <a href="https://github.com/gitlab.scai.fraunhofer/gitlab.scai.fraunhofer/blob/main/LICENSE">
        <img alt="PyPI - License" src="https://img.shields.io/pypi/l/contnextViewer" />
    </a>
    <a href='https://contnextViewer.readthedocs.io/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/contnextViewer/badge/?version=latest' alt='Documentation Status' />
    </a>
    <a href='https://github.com/psf/black'>
        <img src='https://img.shields.io/badge/code%20style-black-000000.svg' alt='Code style: black' />
    </a>
</p>

### ContNeXt WebApp

## 💪 Getting Started

ContNeXt is web application that allows the exploration of comprehensive context-specific portraits of biological processes using gene expression data, and the change in such portraits across different contexts.

## Command Line Interface

The ContNeXt Viewer command line tool is automatically installed. It can
be used from the shell with the `--help` flag to show all subcommands:

```shell
$ contnext_viewer --help
```

To load the contnextViewer database, use the `load` command:
```shell
$ contnext_viewer load [--source /path/to/network/data/directory ]
```
If no source path is given, contnextViewer automatically downloads the necessary data from the project's Zenodo's page [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5831786.svg)](https://doi.org/10.5281/zenodo.5831786).

To load the contnextViewer database, use the `web` command:
```shell
$ contnext_viewer web [--host 0.0.0.0 ] [ --port 5000 ] [ --template path/to/template] [ --static path/tp/static]
```

## 🚀 Installation

<!-- Uncomment this section after your first ``tox -e finish``
The most recent release can be installed from
[PyPI](https://pypi.org/project/contnextViewer/) with:

```bash
$ pip install contnext_viewer
```
-->

The most recent code and data can be installed directly from GitHub with:

```bash
$ pip install git+https://github.com/ContNeXt/web_app.git
```

To install in development mode, use the following:

```bash
$ git clone git+https://github.com/ContNeXt/web_app.git
$ cd web_app.git
$ pip install -e .
```

## ContNeXt Data

ContNeXt's data can be downloaded directly from the project's Zenodo page [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5831786.svg)](https://doi.org/10.5281/zenodo.5831786).

To correctly load the ContNeXt Viewer database, the source data must have 
the following structure:
```
.
├── node_properties
│   ├── tissue
│   │   ├── 0000001 
│   │   │ 	└── node_properties.tsv
│   │   ├── 0000002
│   │   │	└── node_properties.tsv
│   │   └── ... 
│   │
│   ├── cell_line
│   │   ├── 0000003 
│   │   │ 	└── node_properties.tsv
│   │   ├── 0000004
│   │   │	└── node_properties.tsv
│   │   └── ... 
│   │
│   ├── cell_type
│	│   ├── 0000005 
│   │   │	└── node_properties.tsv
│	│   ├── 0000006
│   │   │	└── node_properties.tsv
│   │   └── ... 
│   │
│   └── interactome
│	    └── node_properties.tsv
│
├── coexpr_networks
│   ├── tissue
│   │   ├── 0000001 
│   │   │   └── coexp_network_edges.tsv
│   │   ├── 0000002
│   │   │   └── coexp_network_edges.tsv
│   │   └── ... 
│   │
│   ├── cell_type
│   │   ├── 0000003 
│   │   │   └── coexp_network_edges.tsv
│   │   ├── 0000004
│   │   │   └── coexp_network_edges.tsv
│   │   └── ... 
│   │
│   └── cell_line
│       ├── 0000005 
│       │   └── coexp_network_edges.tsv
│       ├── 0000006
│       │   └── coexp_network_edges.tsv
│       └── ... 
│
├── misc_data
│   ├── tissue_overview.tsv
│   ├── celltype_overview.tsv
│   ├── cellline_overview.tsv
│   ├── tissue_node_degree.tsv
│   ├── celltype_node_degree.tsv
│   └── cellline_node_degree.tsv
│
└── interactome
    ├── interactome_edges.tsv
    └── ... 
    

```
## 👐 Contributing

Contributions, whether filing an issue, making a pull request, or forking, are appreciated. See
[CONTRIBUTING.rst](https://github.com/ContNeXt/web_app/blob/master/CONTRIBUTING.rst) for more information on getting involved.

## 👋 Attribution

### ⚖️ License

The code in this package is licensed under the MIT License.

<!--
### 📖 Citation

Citation goes here!
-->

<!--
### 🎁 Support

This project has been supported by the following organizations (in alphabetical order):

- [Harvard Program in Therapeutic Science - Laboratory of Systems Pharmacology](https://hits.harvard.edu/the-program/laboratory-of-systems-pharmacology/)

-->

<!--
### 💰 Funding

This project has been supported by the following grants:

| Funding Body                                             | Program                                                                                                                       | Grant           |
|----------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|-----------------|
| DARPA                                                    | [Automating Scientific Knowledge Extraction (ASKE)](https://www.darpa.mil/program/automating-scientific-knowledge-extraction) | HR00111990009   |
-->

### 🍪 Cookiecutter

This package was created with [@audreyfeldroy](https://github.com/audreyfeldroy)'s
[cookiecutter](https://github.com/cookiecutter/cookiecutter) package using [@cthoyt](https://github.com/cthoyt)'s
[cookiecutter-snekpack](https://github.com/cthoyt/cookiecutter-snekpack) template.

## 🛠️ For Developers

<details>
  <summary>See developer instrutions</summary>

  
The final section of the README is for if you want to get involved by making a code contribution.

### ❓ Testing

After cloning the repository and installing `tox` with `pip install tox`, the unit tests in the `tests/` folder can be
run reproducibly with:

```shell
$ tox
```

Additionally, these tests are automatically re-run with each commit in a [GitHub Action](https://github.com/ContNeXt/web_app/actions?query=workflow%3ATests).

### 📦 Making a Release

After installing the package in development mode and installing
`tox` with `pip install tox`, the commands for making a new release are contained within the `finish` environment
in `tox.ini`. Run the following from the shell:

```shell
$ tox -e finish
```

This script does the following:

1. Uses BumpVersion to switch the version number in the `setup.cfg` and
   `src/contnext_viewer/version.py` to not have the `-dev` suffix
2. Packages the code in both a tar archive and a wheel
3. Uploads to PyPI using `twine`. Be sure to have a `.pypirc` file configured to avoid the need for manual input at this
   step
4. Push to GitHub. You'll need to make a release going with the commit where the version was bumped.
5. Bump the version to the next patch. If you made big changes and want to bump the version by minor, you can
   use `tox -e bumpversion minor` after.
</details>
