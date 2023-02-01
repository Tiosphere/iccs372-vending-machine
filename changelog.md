# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## 2023-01-29

### Changed
- config workflow and coverage path

### Added
- install coverage lib


## 2023-01-27

### Changed
- remove unused variables in tests
- change variables name in signal
- minor fix

### Added
- add sonar setup


## 2023-01-26

### Changed 
- remove redundant operation in stock views

### Added
- add test for snack views
- add test for stock view


## 2023-01-25

### changed
- fix some bugs
- change method check with string to enum class
- change variables name to be easily understand
- change view functions name to end with 'view'

### Added
- add test for machine and machine instance views


## 2023-01-21

### Added
- add test for models
- add test for serializers


## 2023-01-17

### Changed
- add more status code
- change stock snack_fk relation to CASCADE


## 2023-01-16

### Changed
- add new field to serializer
- fix static warning

### Added
- can search machine by name and location
- add document for machine, machine_instance, snack, and snack_instance endpoint
- add features section into readme


## 2023-01-15

### Changed
- disable csrf token check
- fix create_sample same stock bug

### Added
- add unique constraint to fields in Machine and Snack model
- add signal to auto set status of Machine
- create form and serializer
- create management commands
    - create_sample: to create simple sample data
    - easy_setup: auto migrate and create simple sample data
- add api endpoint for Snack, Machine, and Stock model
- about section in readme file
- add name field to Machine model


## 2023-01-14

### Added
- create models
    - Machine
    - Snack
    - Stock
- requirements.txt


## 2023-01-13

### Changed
- add gitignore

### Added
- new app "myapp"
- start django project
- config setting, urls for "myapp"