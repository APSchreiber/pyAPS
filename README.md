# pyAPS

## Summary

A Python library for customizing ArcPy and ArcGIS.

## Installation

Install by adding the pyAPS.py to the Lib folder in your Python installation directory.

Alternataly, you can run the installer `Installer.py` file found in this project.

### Dependencies

- ArcPy (Installed with ArcGIS)
- PIL (www.pythonware.com/products/pil/)

## Methods

### Ground to Grid

Moves point features based on a scale factor

ground_to_grid(workspace, fc, factor, {where_clause})

| Parameter | Explanation | Data Type |
|---|---|---|
|Workspace|The ArcGIS Workspace containing the data|Workspace or Dataset|
|fc|The name of the feature class|String|
|factor|Scale factor by which to move point|Float|
|where_clause|Where clause to select data to be modified|String|

## Credits

Developed by Andrew Schrieber, Horner & Shifrin