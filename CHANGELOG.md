# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and
this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) when possible.

## [1.0.1] - 2025-11-22

### Added

- Added `ultra_piston.utils.MISSING`

### Fixed

- Fixed various type annotation errors in `ultra_piston.http_clients`.
- Fixed documentation of data models.

## [1.0.0] - 2025-06-29

### Added

- Added main interface client: `ultra_piston.PistonClient`
- Added ABC `ultra_piston.http_clients.AbstractHTTPClient`
- Added HTTP driver `ultra_piston.http_clients.HTTPXClient`
- Added data model `ultra_piston.Runtime`
- Added data model `ultra_piston.Package`
- Added data model `ultra_piston.File`
- Added data model `ultra_piston.RunStage`
- Added data model `ultra_piston.CompileStage`
- Added data model `ultra_piston.ExecutionOutput`
- Added exception `ultra_piston.errors.BasePistonError`
- Added exception `ultra_piston.errors.InternalError`
- Added exception `ultra_piston.errors.ServerError`
- Added exception `ultra_piston.errors.MissingDataError`
- Added exception `ultra_piston.errors.BadRequestError`
- Added exception `ultra_piston.errors.TooManyRequestsError`
- Added exception `ultra_piston.errors.InternalServerError`
- Added exception `ultra_piston.errors.NotFoundError`
- Added exception `ultra_piston.errors.UnexpectedStatusError`
