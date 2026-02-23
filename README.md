# Artifact repository

This repository contains evaluation artifacts for the short paper **Identifying Microcontroller Architecture Through Static Analysis of Firmware Binaries** submitted to SDIoTSec 2026.´

## Check out the original paper!

You can find the paper here:

https://www.ndss-symposium.org/wp-content/uploads/sdiotsec26-7.pdf

## Further development

The code in this replication package will not change to ensure reproducibility in the future. Further development of the tools take place in the following repositories:

* https://github.com/logsincostan/svdmap
* https://github.com/logsincostan/ortellius


## Organization of this repository
* `evaluation.md` contains a detailed explanation of the performed evaluation. In particular, it contains information on how the firmware binaries have been obtained and the calculations behind the statistics presented in the paper.
* `input/` contains the firmware binaries used for the evaluation.
* `knowledge_base/` contains all knowledge bases used in the evaluation.
    * `knowledge_base/svds.tar.gz` is a collection of SVD files collected from
        * https://github.com/cmsis-svd/cmsis-svd-data
        * and scraped from Keil.
    * `knowledge_base/memory_maps_cmsis.tar.gz` are memory maps calculated from `cmsis-svd-data`.
    * `knowledge_base/memory_maps_keil.tar.gz` are memory maps calculated from Keil.
    * `knowledge_base/memory_maps.tar.gz` are memory maps calculated from both `cmsis-svd-data` and Keil.
    * `knowledge_base/shadow_maps_cmsis.tar.gz` are shadow maps calculated from `cmsis-svd-data`.
    * `knowledge_base/shadow_maps_keil.tar.gz` are shadow maps calculated from Keil.
    * `knowledge_base/shadow_maps.tar.gz` are shadow maps calculated from both `cmsis-svd-data` and Keil.
* `output/` contains access maps for all firmware binaries in `input/`
    * Each `.json` access map in `output/` is accompanied by a directory with the same name containing the matching results using different shadow maps.

## Setting up your environment
The precomputed evaluation artifacts already lie in this repository. However, you can follow the steps below to rebuild the artifacts yourself.

### Setting up your environment
To run the evaluation, first create and enter a python venv:

```sh
$ python3 -m venv venv
$ source ./venv/bin/activate
```

Then install pip dependencies:

```sh
$ pip install -r requirements.txt
```

#### Additional requirements.
You need a Java JDK (not JRE!) installed to calculate access maps, as that requires Ghidra.

#### Rebuild SVD collection
A pre-scraped SVD collection can be found in `knowledge_base/svds.tar.gz`. You can rebuild it with

```sh
$ make -B knowledge_base/svds.tar.gz
```

This will take a long time.

#### Rebuild memory maps
The memory maps can be rebuilt with

```sh
$ make knowledge_base/memory_maps.tar.gz
$ make knowledge_base/memory_maps_cmsis.tar.gz
$ make knowledge_base/memory_maps_keil.tar.gz
```

This might take a long time.

#### Rebuild shadow maps
The shadow maps can be rebuilt with

```sh
$ make knowledge_base/shadow_maps.tar.gz
$ make knowledge_base/shadow_maps_cmsis.tar.gz
$ make knowledge_base/shadow_maps_keil.tar.gz
```

This might take a long time.

#### Rebuild access maps
The access maps can be rebuilt with

```sh
$ python ./tools/build_access_maps.py input/fuzzware_samples/ outputs/fuzzware
$ python ./tools/build_access_maps.py input/edgeimpulse/ outputs/edgeimpulse
```

#### Recalculate rankings
The rankings can be recalculated with

```sh
$ python ./tools/rank_shadows.py outputs/ knowledge_base/
```

#### Count shadow maps in knowledge base
To count the number of shadow maps in a knowledge base, run one of:

```sh
$ python tools/count_shadow_maps.py knowledge_base/shadow_maps.tar.gz
$ python tools/count_shadow_maps.py knowledge_base/shadow_maps_keil.tar.gz
$ python tools/count_shadow_maps.py knowledge_base/shadow_maps_cmsis.tar.gz
```

This will output both the total number of of shadow maps in the knowledge base as well as the number of shadow maps that can be distinguished solely by their read and write accesses.