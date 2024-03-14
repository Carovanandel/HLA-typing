# Changelog

<!--
Newest changes should be on top.

This document is user facing. Please word the changes in such a way
that users understand how the changes affect the new version.
-->

## v1.2.0
+ Update to snakemake 8.4
+ Remove default configuration

## v1.1.0
+ Update to snakemake 7.3
+ Remove settings from the PEP configuration
+ Switch to simplified PEP configuration (a csv is valid PEP)
+ Reduce wait time for missing files to 5 seconds
+ Keep temporary and failed files, to aid in debugging

## v0.0.1
+ Add support for project configuration using
[PEP](http://pep.databio.org/en/latest/).
+ Add integration tests using pytest-workflow and github workflows.
