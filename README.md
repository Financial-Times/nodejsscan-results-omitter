# nodejsscan-results-omitter

A python script which takes the results from [NodeJsScan](https://github.com/ajinabraham/NodeJsScan). It allows you to omit findings from certain directories as well as skipping any false positives that may have been found during the scan.

This was developed for and used in [nodejsscan-orb](https://github.com/Financial-Times/nodejsscan-orb) so this module is automatically included when you use the orb. In most cases, you will **NOT** have to install this module yourself.

## Requirements
This module was developed for Python3 and doesn't use any non standard modules.

## Installation
`pip install git+https://github.com/Financial-Times/nodejsscan-results-omitter`

## Usage
This module will look for a file called `results.json` in the current working directory. It will parse the file and if there are any security issues it will return an exit code of 1. This is useful if you want to fail a CI build when security issues are present.

If you want to ignore issues based on path, type of issue, or issue hash then you can choose to ignore them. To make use of this functionality, create a configuration file called ```.nodejsscan.json``` in the root directiory of the repository. Examples of how to add entries to exclude paths, findings and titles is shown below:

```
{
    "exclude": {
        "path": ["test/*"]
        "hash": ["da0caf9f5c5eba0384ae977316d05d943e4166cdffdba3b36717d830dd96e407"]
        "title": ["Secret Hardcoded"]
    }
}
```
