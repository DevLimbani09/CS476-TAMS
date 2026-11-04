_Last updated: 2026-11-03_
# Architectural Decision Records

This document aims to keep track of all the decisions made during our group meeting. In case there is a confusion as to why a certain task was done a certain way this document should be refered as it will be working as a history log.

---

## Overview

The general strucute of this document would be:
##### ADR# Decision Title #####
Each ADR will follow the structure below:

ADR-XXX: Decision Title

Date: Date of the decision

Status: Proposed / Accepted / Superseded / Rejected

Context: Describe the problem, requirements, or constraints that led to the decision.

Options Considered: Identify the alternatives evaluated by the team.

Decision: State the selected approach and why.

Conclusion

## Logs

### ADR#001 Storage system ###

Date: 21st of September, 2026

Status: Accepted

Context:
When starting the project our basic question was to where will we be storing the project. Our requirements were to leverage any solution which University provides us, so that it is easier for us to manage the financial aspects of this project.

Therefore we ended up choosing as Microsoft OneDrive as our cloud storage solution because it is already included in our University M365 licenses.Furthermore, Github will be used primarily as our source code and version control software as it is a mandatory for this software.

Options Considered: 
- Microsoft One Drive: Cloud storage provided through the university's Microsoft 365 subscription.
- Google Drive:  An alternative cloud storage platform supporting document sharing and collaboration.

Decision: Microsoft One Drive. We will be using Microsoft Drive as it is readily available functionality within our university.

### ADR#002 Version Control system ###

Date: 21st of September, 2026

Status: Accepted

Context:
As per the project requirement we do not have much of a selection task here we will be using Github for our version control.

Decision: Github

### ADR#003.1 MVC Architecture Stack Selection ###

Date: 6th of October, 2026

Status: Accepted

Context: As per the project requirements the employee time card management system is required to follow a Model-View-Context Architecture. Therefore we needed to select a web development framework which can be used to implement the software. 

During the selection process, we considered several frameworks and programming languages. The primary considerations were the popularity of the programming language, availability of learning resources, long-term maintainability, security, and the frequency of framework updates.

Options Considered:
- ASP.NET Core MVC — C#: A web development framework developed by Microsoft that follows the Model-View-Controller (MVC) architectural pattern.
- Django MVT — Python: A Python-based web framework that follows the Model-View-Template (MVT) architectural pattern.
- Laravel MVC — PHP: A PHP-based web framework that follows the Model-View-Controller (MVC) architectural pattern.
- Spring MVC — Java: A Java-based web framework that follows the Model-View-Controller (MVC) architectural pattern. 

Decison: We decided to use Python with the Django framework, following the Model-View-Template (MVT) architectural pattern. This is because python is the most popular language therefore, it is bound to have an abundance of educational resources, documentation, and tutorials, which helps us to learn the language, troubleshoot problems faster.

### ADR#003.2 Database Selection ###

Date: 6th of October, 2026

Status: Accepted

Context:
We need a reliable database management system to store and manage employee information, timecards, working hours, leave requests, and account credentials. The team needed a database solution that would be easy to integrate with the Django framework, provide reliable data management, and minimize hosting costs.

Options Considered: 
- PostgreSQL: A popular open source relational database management system.
- MySQL: A widely used in the industry open-source relational database management system
- SQLite: A lightweight relational database included with Django by default, suitable for development and smaller applications.

Decison: PostgreSQL was selected due to its reliability, maintainability, and ability to support concurrent access from multiple users. Although Django includes SQLite by default, SQLite stores its database in a local file, which introduces additional challenges when sharing a database across multiple application servers or recovering from server failures.

### ADR#004 Workflow ###


