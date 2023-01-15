# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## 2023-01-15

### Changed
- disable csrf token check

### Added
- add unique constraint to fields in Machine and Snack model
- add signal to auto set status of Machine
- create form and serializer
- create management commands
    - create_sample: to create simple sample data
    - easy_setup: auto migrate and create simple sample data
- add api endpoint for Snack and Machine model
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