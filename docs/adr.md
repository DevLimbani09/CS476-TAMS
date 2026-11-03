_Last updated: 2026-10-04_
# Architectural Decision Records

This document aims to keep track of all the decisions made during our group meeting. In case there is a confusion as to why a certain task was done a certain way this document should be refered as it will be working as a history log.

---

## Overview

The general strucute of this document would be:
##### ADR# Decision Title #####
Decision description <br>

Conclusion

## Logs

##### ADR#001 Storage system #####
When starting the project our basic question was to where will we be storing the project. Our requirements were to leverage any solution which University provides us, so that it is easier for us to manage the financial aspects of this project.<br>

Therefore we ended up choosing as Microsoft OneDrive as our cloud storage solution because it is already included in our University M365 licenses.Furthermore, Github will be used primarily as our source code and version control software as it is a mandatory for this software.

##### ADR#002 Version Control system #####
The basic idea is that w