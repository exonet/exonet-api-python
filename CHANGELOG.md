# Changelog

All notable changes to `exonet-api-python` will be documented in this file.

Updates should follow the [Keep a CHANGELOG](http://keepachangelog.com/) principles.

## [Unreleased]
[Compare 2.0.0 - Unreleased](https://github.com/exonet/exonet-api-python/compare/2.0.0...master)
### Breaking
- Return None when a relation which doesn't exists is retrieved.

## [2.1.0](https://github.com/exonet/exonet-api-python/releases/tag/2.1.0) - 2019-11-19
[Compare 2.0.0 - 2.1.0](https://github.com/exonet/exonet-api-python/compare/2.0.0...2.1.0)
### Changed
- Extend the `ValidationException` to contain all returned validation errors. See the [docs](./docs/error_handling.md) for more information.

## [2.0.0](https://github.com/exonet/exonet-api-python/releases/tag/2.0.0) - 2019-09-19
[Compare 1.0.0 - 2.0.0](https://github.com/exonet/exonet-api-python/compare/1.0.0...2.0.0)
### Breaking
- The `Api` prefix has been added from the following classes for consistency:
  - `Resource` --> `ApiResource`
  - `ResourceIdentifier` --> `ApiResourceIdentifier`
  
### Added
- Support for `PATCH` and `DELETE` requests.

### Deprecated
- The `store` method for creating `POST` requests is now deprecated. Use `post` instead.

## [1.0.0](https://github.com/exonet/exonet-api-python/releases/tag/1.0.0) - 2019-08-14
[Compare 0.0.5 - 1.0.0](https://github.com/exonet/exonet-api-python/compare/0.0.5...1.0.0)
## Breaking
- The Client has been refactored to keep consistency between packages in different programming languages. See the updated documentation and examples.

## [0.0.5](https://github.com/exonet/exonet-api-python/releases/tag/0.0.5) - 2019-04-29
[Compare 0.0.4 - 0.0.5](https://github.com/exonet/exonet-api-python/compare/0.0.4...0.0.5)
### Added
- Examples to use the DNS endpoints.

## [0.0.4](https://github.com/exonet/exonet-api-python/releases/tag/0.0.4) - 2018-11-19
[Compare 0.0.3 - 0.0.4](https://github.com/exonet/exonet-api-python/compare/0.0.3...0.0.4)
### Added
- Sort by field.

## [0.0.3](https://github.com/exonet/exonet-api-python/releases/tag/0.0.3) - 2018-06-26
[Compare 0.0.2 - 0.0.3](https://github.com/exonet/exonet-api-python/compare/0.0.2...0.0.3)
### Added
- Ready to use examples to get ticket details.
- Individual methods to set or get relationships from a resource object.

### Changed
- Most class variables changed to instance variables.
  This enforces the defaults to be set, instead of using the same variables from another instance.

## [0.0.2](https://github.com/exonet/exonet-api-python/releases/tag/0.0.2) - 2018-05-23
[Compare 0.0.1 - 0.0.2](https://github.com/exonet/exonet-api-python/compare/0.0.1...0.0.2)
### Fixed
- Parse dict as relationship.

## [0.0.1](https://github.com/exonet/exonet-api-python/releases/tag/0.0.1) - 2018-03-23
### Added
- Initial release.
