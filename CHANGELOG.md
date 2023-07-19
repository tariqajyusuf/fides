# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/)

The types of changes are:

- `Added` for new features.
- `Changed` for changes in existing functionality.
- `Developer Experience` for changes in developer workflow or tooling.
- `Deprecated` for soon-to-be removed features.
- `Docs` for documentation only changes.
- `Removed` for now removed features.
- `Fixed` for any bug fixes.
- `Security` in case of vulnerabilities.

## [Unreleased](https://github.com/ethyca/fides/compare/2.17.0...main)

## [2.17.0](https://github.com/ethyca/fides/compare/2.16.0...2.17.0)

### Added

- Tab component for `fides-js` [#3782](https://github.com/ethyca/fides/pull/3782)
- Prefetches API calls as part of Fides.js [#3698](https://github.com/ethyca/fides/pull/3698)

### Developer Experience

- Changed where db-dependent routers were imported to avoid dependency issues [#3741](https://github.com/ethyca/fides/pull/3741)

### Changed

- Bumped supported Python versions to `3.10.12`, `3.9.17`, and `3.8.17` [#3733](https://github.com/ethyca/fides/pull/3733)
- Logging Updates [#3758](https://github.com/ethyca/fides/pull/3758)
- Add polyfill service to fides-js route [#3759](https://github.com/ethyca/fides/pull/3759)
- Show/hide integration values [#3775](https://github.com/ethyca/fides/pull/3775)
- Sort system cards alphabetically by name on "View systems" page [#3781](https://github.com/ethyca/fides/pull/3781)
- Update admin ui to use new integration delete route [#3785](https://github.com/ethyca/fides/pull/3785)

### Removed

- Removed "Custom field(s) successfully saved" toast [#3779](https://github.com/ethyca/fides/pull/3779)

### Added

- Record when consent is served [#3777](https://github.com/ethyca/fides/pull/3777)
- Add an `active` property to taxonomy elements [#3784](https://github.com/ethyca/fides/pull/3784)
- Erasure support for Heap [#3599](https://github.com/ethyca/fides/pull/3599)

### Fixed
- Privacy notice UI's list of possible regions now matches the backend's list [#3787](https://github.com/ethyca/fides/pull/3787)
- Admin UI "property does not existing" build issue [#3831](https://github.com/ethyca/fides/pull/3831)

## [2.16.0](https://github.com/ethyca/fides/compare/2.15.1...2.16.0)

### Added

- Empty state for when there are no relevant privacy notices in the privacy center [#3640](https://github.com/ethyca/fides/pull/3640)
- GPC indicators in fides-js banner and modal [#3673](https://github.com/ethyca/fides/pull/3673)
- Include `data_use` and `data_category` metadata in `upload` of access results [#3674](https://github.com/ethyca/fides/pull/3674)
- Add enable/disable toggle to integration tab [#3593] (https://github.com/ethyca/fides/pull/3593)

### Fixed

- Render linebreaks in the Fides.js overlay descriptions, etc. [#3665](https://github.com/ethyca/fides/pull/3665)
- Broken link to Fides docs site on the About Fides page in Admin UI [#3643](https://github.com/ethyca/fides/pull/3643)
- Add Systems Applicable Filter to Privacy Experience List [#3654](https://github.com/ethyca/fides/pull/3654)
- Privacy center and fides-js now pass in `Unescape-Safestr` as a header so that special characters can be rendered properly [#3706](https://github.com/ethyca/fides/pull/3706)
- Fixed ValidationError for saving PrivacyPreferences [#3719](https://github.com/ethyca/fides/pull/3719)
- Fixed issue preventing ConnectionConfigs with duplicate names from saving [#3770](https://github.com/ethyca/fides/pull/3770)
- Fixed creating and editing manual integrations [#3772](https://github.com/ethyca/fides/pull/3772) 
- Fix lingering integration artifacts by cascading deletes from System [#3771](https://github.com/ethyca/fides/pull/3771)

### Developer Experience

- Reorganized some `api.api.v1` code to avoid circular dependencies on `quickstart` [#3692](https://github.com/ethyca/fides/pull/3692)
- Treat underscores as special characters in user passwords [#3717](https://github.com/ethyca/fides/pull/3717)
- Allow Privacy Notices banner and modal to scroll as needed [#3713](https://github.com/ethyca/fides/pull/3713)
- Make malicious url test more robust to environmental differences [#3748](https://github.com/ethyca/fides/pull/3748)
- Ignore type checker on click decorators to bypass known issue with `click` version `8.1.4` [#3746](https://github.com/ethyca/fides/pull/3746)

### Changed

- Moved GPC preferences slightly earlier in Fides.js lifecycle [#3561](https://github.com/ethyca/fides/pull/3561)
- Changed results from clicking "Test connection" to be a toast instead of statically displayed on the page [#3700](https://github.com/ethyca/fides/pull/3700)
- Moved "management" tab from nav into settings icon in top right [#3701](https://github.com/ethyca/fides/pull/3701)
- Remove name and description fields from integration form [#3684](https://github.com/ethyca/fides/pull/3684)
- Update EU PrivacyNoticeRegion codes and allow experience filtering to drop back to country filtering if region not found [#3630](https://github.com/ethyca/fides/pull/3630)
- Fields with default fields are now flagged as required in the front-end [#3694](https://github.com/ethyca/fides/pull/3694)
- In "view systems", system cards can now be clicked and link to that system's `configure/[id]` page [#3734](https://github.com/ethyca/fides/pull/3734)
- Enable privacy notice and privacy experience feature flags by default [#3773](https://github.com/ethyca/fides/pull/3773)

### Security
- Resolve Zip bomb file upload vulnerability [CVE-2023-37480](https://github.com/ethyca/fides/security/advisories/GHSA-g95c-2jgm-hqc6)
- Resolve SVG bomb (billion laughs) file upload vulnerability [CVE-2023-37481](https://github.com/ethyca/fides/security/advisories/GHSA-3rw2-wfc8-wmj5)

## [2.15.1](https://github.com/ethyca/fides/compare/2.15.0...2.15.1)

### Added
- Set `sslmode` to `prefer` if connecting to Redshift via ssh [#3685](https://github.com/ethyca/fides/pull/3685)

### Changed
- Privacy center action cards are now able to expand to accommodate longer text [#3669](https://github.com/ethyca/fides/pull/3669)
- Update integration endpoint permissions [#3707](https://github.com/ethyca/fides/pull/3707)

### Fixed
- Handle names with a double underscore when processing access and erasure requests [#3688](https://github.com/ethyca/fides/pull/3688)
- Allow Privacy Notices banner and modal to scroll as needed [#3713](https://github.com/ethyca/fides/pull/3713)

### Security
- Resolve path traversal vulnerability in webserver API [CVE-2023-36827](https://github.com/ethyca/fides/security/advisories/GHSA-r25m-cr6v-p9hq)

## [2.15.0](https://github.com/ethyca/fides/compare/2.14.1...2.15.0)

### Added

- Privacy center can now render its consent values based on Privacy Notices and Privacy Experiences [#3411](https://github.com/ethyca/fides/pull/3411)
- Add Google Tag Manager and Privacy Center ENV vars to sample app [#2949](https://github.com/ethyca/fides/pull/2949)
- Add `notice_key` field to Privacy Notice UI form [#3403](https://github.com/ethyca/fides/pull/3403)
- Add `identity` query param to the consent reporting API view [#3418](https://github.com/ethyca/fides/pull/3418)
- Use `rollup-plugin-postcss` to bundle and optimize the `fides.js` components CSS [#3411](https://github.com/ethyca/fides/pull/3411)
- Dispatch Fides.js lifecycle events on window (FidesInitialized, FidesUpdated) and cross-publish to Fides.gtm() integration [#3411](https://github.com/ethyca/fides/pull/3411)
- Added the ability to use custom CAs with Redis via TLS [#3451](https://github.com/ethyca/fides/pull/3451)
- Add default experience configs on startup [#3449](https://github.com/ethyca/fides/pull/3449)
- Load default privacy notices on startup [#3401](https://github.com/ethyca/fides/pull/3401)
- Add ability for users to pass in additional parameters for application database connection [#3450](https://github.com/ethyca/fides/pull/3450)
- Load default privacy notices on startup [#3401](https://github.com/ethyca/fides/pull/3401/files)
- Add ability for `fides-js` to make API calls to Fides [#3411](https://github.com/ethyca/fides/pull/3411)
- `fides-js` banner is now responsive across different viewport widths [#3411](https://github.com/ethyca/fides/pull/3411)
- Add ability to close `fides-js` banner and modal via a button or ESC [#3411](https://github.com/ethyca/fides/pull/3411)
- Add ability to open the `fides-js` modal from a link on the host site [#3411](https://github.com/ethyca/fides/pull/3411)
- GPC preferences are automatically applied via `fides-js` [#3411](https://github.com/ethyca/fides/pull/3411)
- Add new dataset route that has additional filters [#3558](https://github.com/ethyca/fides/pull/3558)
- Update dataset dropdown to use new api filter [#3565](https://github.com/ethyca/fides/pull/3565)
- Filter out saas datasets from the rest of the UI [#3568](https://github.com/ethyca/fides/pull/3568)
- Included optional env vars to have postgres or Redshift connected via bastion host [#3374](https://github.com/ethyca/fides/pull/3374/)
- Support for acknowledge button for notice-only Privacy Notices and to disable toggling them off [#3546](https://github.com/ethyca/fides/pull/3546)
- HTML format for privacy request storage destinations [#3427](https://github.com/ethyca/fides/pull/3427)
- Persistent message showing result and timestamp of last integration test to "Integrations" tab in system view [#3628](https://github.com/ethyca/fides/pull/3628)
- Access and erasure support for SurveyMonkey [#3590](https://github.com/ethyca/fides/pull/3590)
- New Cookies Table for storing cookies associated with systems and privacy declarations [#3572](https://github.com/ethyca/fides/pull/3572)
- `fides-js` and privacy center now delete cookies associated with notices that were opted out of [#3569](https://github.com/ethyca/fides/pull/3569)
- Cookie input field on system data use tab [#3571](https://github.com/ethyca/fides/pull/3571)

### Fixed

- Fix sample app `DATABASE_*` ENV vars for backwards compatibility [#3406](https://github.com/ethyca/fides/pull/3406)
- Fix overlay rendering issue by finding/creating a dedicated parent element for Preact [#3397](https://github.com/ethyca/fides/pull/3397)
- Fix the sample app privacy center link to be configurable [#3409](https://github.com/ethyca/fides/pull/3409)
- Fix CLI output showing a version warning for Snowflake [#3434](https://github.com/ethyca/fides/pull/3434)
- Flaky custom field Cypress test on systems page [#3408](https://github.com/ethyca/fides/pull/3408)
- Fix NextJS errors & warnings for Cookie House sample app [#3411](https://github.com/ethyca/fides/pull/3411)
- Fix bug where `fides-js` toggles were not reflecting changes from rejecting or accepting all notices [#3522](https://github.com/ethyca/fides/pull/3522)
- Remove the `fides-js` banner from tab order when it is hidden and move the overlay components to the top of the tab order. [#3510](https://github.com/ethyca/fides/pull/3510)
- Fix bug where `fides-js` toggle states did not always initialize properly [#3597](https://github.com/ethyca/fides/pull/3597)
- Fix race condition with consent modal link rendering [#3521](https://github.com/ethyca/fides/pull/3521)
- Hide custom fields section when there are no custom fields created [#3554](https://github.com/ethyca/fides/pull/3554)
- Disable connector dropdown in integration tab on save [#3552](https://github.com/ethyca/fides/pull/3552)
- Handles an edge case for non-existent identities with the Kustomer API [#3513](https://github.com/ethyca/fides/pull/3513)
- remove the configure privacy request tile from the home screen [#3555](https://github.com/ethyca/fides/pull/3555)
- Updated Privacy Experience Safe Strings Serialization [#3600](https://github.com/ethyca/fides/pull/3600/)
- Only create default experience configs on startup, not update [#3605](https://github.com/ethyca/fides/pull/3605)
- Update to latest asyncpg dependency to avoid build error [#3614](https://github.com/ethyca/fides/pull/3614)
- Fix bug where editing a data use on a system could delete existing data uses [#3627](https://github.com/ethyca/fides/pull/3627)
- Restrict Privacy Center debug logging to development-only [#3638](https://github.com/ethyca/fides/pull/3638)
- Fix bug where linking an integration would not update the tab when creating a new system [#3662](https://github.com/ethyca/fides/pull/3662)
- Fix dataset yaml not properly reflecting the dataset in the dropdown of system integrations tab [#3666](https://github.com/ethyca/fides/pull/3666)
- Fix privacy notices not being able to be edited via the UI after the addition of the `cookies` field [#3670](https://github.com/ethyca/fides/pull/3670)
- Add a transform in the case of `null` name fields in privacy declarations for the data use forms [#3683](https://github.com/ethyca/fides/pull/3683)

### Changed

- Enabled Privacy Experience beta flag [#3364](https://github.com/ethyca/fides/pull/3364)
- Reorganize CLI Command Source Files [#3491](https://github.com/ethyca/fides/pull/3491)
- Removed ExperienceConfig.delivery_mechanism constraint [#3387](https://github.com/ethyca/fides/pull/3387)
- Updated privacy experience UI forms to reflect updated experience config fields [#3402](https://github.com/ethyca/fides/pull/3402)
- Use a venv in the Dockerfile for installing Python deps [#3452](https://github.com/ethyca/fides/pull/3452)
- Bump SlowAPI Version [#3456](https://github.com/ethyca/fides/pull/3456)
- Bump Psycopg2-binary Version [#3473](https://github.com/ethyca/fides/pull/3473)
- Reduced duplication between PrivacyExperience and PrivacyExperienceConfig [#3470](https://github.com/ethyca/fides/pull/3470)
- Update privacy centre email and phone validation to allow for both to be blank [#3432](https://github.com/ethyca/fides/pull/3432)
- Moved connection configuration into the system portal [#3407](https://github.com/ethyca/fides/pull/3407)
- Update `fideslang` to `1.4.1` to allow arbitrary nested metadata on `System`s and `Dataset`s `meta` property [#3463](https://github.com/ethyca/fides/pull/3463)
- Remove form validation to allow both email & phone inputs for consent requests [#3529](https://github.com/ethyca/fides/pull/3529)
- Removed dataset dropdown from saas connector configuration [#3563](https://github.com/ethyca/fides/pull/3563)
- Removed `pyodbc` in favor of `pymssql` for handling SQL Server connections [#3435](https://github.com/ethyca/fides/pull/3435)
- Only create a PrivacyRequest when saving consent if at least one notice has system-wide enforcement [#3626](https://github.com/ethyca/fides/pull/3626)
- Increased the character limit for the `SafeStr` type from 500 to 32000 [#3647](https://github.com/ethyca/fides/pull/3647)
- Changed "connection" to "integration" on system view and edit pages [#3659](https://github.com/ethyca/fides/pull/3659)

### Developer Experience

- Add ability to pass ENV vars to both privacy center and sample app during `fides deploy` via `.env` [#2949](https://github.com/ethyca/fides/pull/2949)
- Handle an edge case when generating tags that finds them out of sequence [#3405](https://github.com/ethyca/fides/pull/3405)
- Add support for pushing `prerelease` and `rc` tagged images to Dockerhub [#3474](https://github.com/ethyca/fides/pull/3474)
- Optimize GitHub workflows used for docker image publishing [#3526](https://github.com/ethyca/fides/pull/3526)

### Removed

- Removed the deprecated `system_dependencies` from `System` resources, migrating to `egress` [#3285](https://github.com/ethyca/fides/pull/3285)

### Docs

- Updated developer docs for ARM platform users related to `pymssql` [#3615](https://github.com/ethyca/fides/pull/3615)

## [2.14.1](https://github.com/ethyca/fides/compare/2.14.0...2.14.1)

### Added

- Add `identity` query param to the consent reporting API view [#3418](https://github.com/ethyca/fides/pull/3418)
- Add privacy centre button text customisations [#3432](https://github.com/ethyca/fides/pull/3432)
- Add privacy centre favicon customisation [#3432](https://github.com/ethyca/fides/pull/3432)

### Changed

- Update privacy centre email and phone validation to allow for both to be blank [#3432](https://github.com/ethyca/fides/pull/3432)

## [2.14.0](https://github.com/ethyca/fides/compare/2.13.0...2.14.0)

### Added

- Add an automated test to check for `/fides-consent.js` backwards compatibility [#3289](https://github.com/ethyca/fides/pull/3289)
- Add infrastructure for "overlay" consent components (Preact, CSS bundling, etc.) and initial version of consent banner [#3191](https://github.com/ethyca/fides/pull/3191)
- Add the modal component of the "overlay" consent components [#3291](https://github.com/ethyca/fides/pull/3291)
- Added an `automigrate` database setting [#3220](https://github.com/ethyca/fides/pull/3220)
- Track Privacy Experience with Privacy Preferences [#3311](https://github.com/ethyca/fides/pull/3311)
- Add ability for `fides-js` to fetch its own geolocation [#3356](https://github.com/ethyca/fides/pull/3356)
- Add ability to select different locations in the "Cookie House" sample app [#3362](https://github.com/ethyca/fides/pull/3362)
- Added optional logging of resource changes on the server [#3331](https://github.com/ethyca/fides/pull/3331)

### Fixed

- Maintain casing differences within Snowflake datasets for proper DSR execution [#3245](https://github.com/ethyca/fides/pull/3245)
- Handle DynamoDB edge case where no attributes are defined [#3299](https://github.com/ethyca/fides/pull/3299)
- Support pseudonymous consent requests with `fides_user_device_id` for the new consent workflow [#3203](https://github.com/ethyca/fides/pull/3203)
- Fides user device id filter to GET Privacy Experience List endpoint to stash user preferences on embedded notices [#3302](https://github.com/ethyca/fides/pull/3302)
- Support for data categories on manual webhook fields [#3330](https://github.com/ethyca/fides/pull/3330)
- Added config-driven rendering to consent components [#3316](https://github.com/ethyca/fides/pull/3316)
- Pin `typing_extensions` dependency to `4.5.0` to work around a pydantic bug [#3357](https://github.com/ethyca/fides/pull/3357)

### Changed

- Explicitly escape/unescape certain fields instead of using SafeStr [#3144](https://github.com/ethyca/fides/pull/3144)
- Updated DynamoDB icon [#3296](https://github.com/ethyca/fides/pull/3296)
- Increased default page size for the connection type endpoint to 100 [#3298](https://github.com/ethyca/fides/pull/3298)
- Data model around PrivacyExperiences to better keep Privacy Notices and Experiences in sync [#3292](https://github.com/ethyca/fides/pull/3292)
- UI calls to support new PrivacyExperiences data model [#3313](https://github.com/ethyca/fides/pull/3313)
- Ensure email connectors respect the `notifications.notification_service_type` app config property if set [#3355](https://github.com/ethyca/fides/pull/3355)
- Rework Delighted connector so the `survey_response` endpoint depends on the `person` endpoint [3385](https://github.com/ethyca/fides/pull/3385)
- Remove logging within the Celery creation function [#3303](https://github.com/ethyca/fides/pull/3303)
- Update how generic endpoint generation works [#3304](https://github.com/ethyca/fides/pull/3304)
- Restrict strack-trace logging when not in Dev mode [#3081](https://github.com/ethyca/fides/pull/3081)
- Refactor CSS variables for `fides-js` to match brandable color palette [#3321](https://github.com/ethyca/fides/pull/3321)
- Moved all of the dirs from `fides.api.ops` into `fides.api` [#3318](https://github.com/ethyca/fides/pull/3318)
- Put global settings for fides.js on privacy center settings [#3333](https://github.com/ethyca/fides/pull/3333)
- Changed `fides db migrate` to `fides db upgrade` [#3342](https://github.com/ethyca/fides/pull/3342)
- Add required notice key to privacy notices [#3337](https://github.com/ethyca/fides/pull/3337)
- Make Privacy Experience List public, and separate public endpoint rate limiting [#3339](https://github.com/ethyca/fides/pull/3339)

### Developer Experience

- Add dispatch event when publishing a non-prod tag [#3317](https://github.com/ethyca/fides/pull/3317)
- Add OpenAPI (Swagger) documentation for Fides Privacy Center API endpoints (/fides.js) [#3341](https://github.com/ethyca/fides/pull/3341)

### Removed

- Remove `fides export` command and backing code [#3256](https://github.com/ethyca/fides/pull/3256)

## [2.13.0](https://github.com/ethyca/fides/compare/2.12.1...2.13.0)

### Added

- Connector for DynamoDB [#2998](https://github.com/ethyca/fides/pull/2998)
- Access and erasure support for Amplitude [#2569](https://github.com/ethyca/fides/pull/2569)
- Access and erasure support for Gorgias [#2444](https://github.com/ethyca/fides/pull/2444)
- Privacy Experience Bulk Create, Bulk Update, and Detail Endpoints [#3185](https://github.com/ethyca/fides/pull/3185)
- Initial privacy experience UI [#3186](https://github.com/ethyca/fides/pull/3186)
- A JavaScript modal to copy a script tag for `fides.js` [#3238](https://github.com/ethyca/fides/pull/3238)
- Access and erasure support for OneSignal [#3199](https://github.com/ethyca/fides/pull/3199)
- Add the ability to "inject" location into `/fides.js` bundles and cache responses for one hour [#3272](https://github.com/ethyca/fides/pull/3272)

### Changed

- Merge instances of RTK `createApi` into one instance for better cache invalidation [#3059](https://github.com/ethyca/fides/pull/3059)
- Update custom field definition uniqueness to be case insensitive name per resource type [#3215](https://github.com/ethyca/fides/pull/3215)
- Restrict where privacy notices of certain consent mechanisms must be displayed [#3195](https://github.com/ethyca/fides/pull/3195)
- Merged the `lib` submodule into the `api.ops` submodule [#3134](https://github.com/ethyca/fides/pull/3134)
- Merged duplicate privacy declaration components [#3254](https://github.com/ethyca/fides/pull/3254)
- Refactor client applications into a monorepo with turborepo, extract fides-js into a standalone package, and improve privacy-center to load configuration at runtime [#3105](https://github.com/ethyca/fides/pull/3105)

### Fixed

- Prevent ability to unintentionally show "default" Privacy Center configuration, styles, etc. [#3242](https://github.com/ethyca/fides/pull/3242)
- Fix broken links to docs site pages in Admin UI [#3232](https://github.com/ethyca/fides/pull/3232)
- Repoint legacy docs site links to the new and improved docs site [#3167](https://github.com/ethyca/fides/pull/3167)
- Fix Cookie House Privacy Center styles for fides deploy [#3283](https://github.com/ethyca/fides/pull/3283)
- Maintain casing differences within Snowflake datasets for proper DSR execution [#3245](https://github.com/ethyca/fides/pull/3245)

### Developer Experience

- Use prettier to format _all_ source files in client packages [#3240](https://github.com/ethyca/fides/pull/3240)

### Deprecated

- Deprecate `fides export` CLI command as it is moving to `fidesplus` [#3264](https://github.com/ethyca/fides/pull/3264)

## [2.12.1](https://github.com/ethyca/fides/compare/2.12.0...2.12.1)

### Changed

- Updated how Docker version checks are handled and added an escape-hatch [#3218](https://github.com/ethyca/fides/pull/3218)

### Fixed

- Datamap export mitigation for deleted taxonomy elements referenced by declarations [#3214](https://github.com/ethyca/fides/pull/3214)
- Update datamap columns each time the page is visited [#3211](https://github.com/ethyca/fides/pull/3211)
- Ensure inactive custom fields are not returned for datamap response [#3223](https://github.com/ethyca/fides/pull/3223)

## [2.12.0](https://github.com/ethyca/fides/compare/2.11.0...2.12.0)

### Added

- Access and erasure support for Aircall [#2589](https://github.com/ethyca/fides/pull/2589)
- Access and erasure support for Klaviyo [#2501](https://github.com/ethyca/fides/pull/2501)
- Page to edit or add privacy notices [#3058](https://github.com/ethyca/fides/pull/3058)
- Side navigation bar can now also have children navigation links [#3099](https://github.com/ethyca/fides/pull/3099)
- Endpoints for consent reporting [#3095](https://github.com/ethyca/fides/pull/3095)
- Added manage custom fields page behind feature flag [#3089](https://github.com/ethyca/fides/pull/3089)
- Custom fields table [#3097](https://github.com/ethyca/fides/pull/3097)
- Custom fields form modal [#3165](https://github.com/ethyca/fides/pull/3165)
- Endpoints to save the new-style Privacy Preferences with respect to a fides user device id [#3132](https://github.com/ethyca/fides/pull/3132)
- Support `privacy_declaration` as a resource type for custom fields [#3149](https://github.com/ethyca/fides/pull/3149)
- Expose `id` field of embedded `privacy_declarations` on `system` API responses [#3157](https://github.com/ethyca/fides/pull/3157)
- Access and erasure support for Unbounce [#2697](https://github.com/ethyca/fides/pull/2697)
- Support pseudonymous consent requests with `fides_user_device_id` [#3158](https://github.com/ethyca/fides/pull/3158)
- Update `fides_consent` cookie format [#3158](https://github.com/ethyca/fides/pull/3158)
- Add custom fields to the data use declaration form [#3197](https://github.com/ethyca/fides/pull/3197)
- Added fides user device id as a ProvidedIdentityType [#3131](https://github.com/ethyca/fides/pull/3131)

### Changed

- The `cursor` pagination strategy now also searches for data outside of the `data_path` when determining the cursor value [#3068](https://github.com/ethyca/fides/pull/3068)
- Moved Privacy Declarations associated with Systems to their own DB table [#3098](https://github.com/ethyca/fides/pull/3098)
- More tests on data use validation for privacy notices within the same region [#3156](https://github.com/ethyca/fides/pull/3156)
- Improvements to export code for bugfixes and privacy declaration custom field support [#3184](https://github.com/ethyca/fides/pull/3184)
- Enabled privacy notice feature flag [#3192](https://github.com/ethyca/fides/pull/3192)
- Updated TS types - particularly with new privacy notices [#3054](https://github.com/ethyca/fides/pull/3054)
- Make name not required on privacy declaration [#3150](https://github.com/ethyca/fides/pull/3150)
- Let Rule Targets allow for custom data categories [#3147](https://github.com/ethyca/fides/pull/3147)

### Removed

- Removed the warning about access control migration [#3055](https://github.com/ethyca/fides/pull/3055)
- Remove `customFields` feature flag [#3080](https://github.com/ethyca/fides/pull/3080)
- Remove notification banner from the home page [#3088](https://github.com/ethyca/fides/pull/3088)

### Fixed

- Fix a typo in the Admin UI [#3166](https://github.com/ethyca/fides/pull/3166)
- The `--local` flag is now respected for the `scan dataset db` command [#3096](https://github.com/ethyca/fides/pull/3096)
- Fixing issue where connectors with external dataset references would fail to save [#3142](https://github.com/ethyca/fides/pull/3142)
- Ensure privacy declaration IDs are stable across updates through system API [#3188](https://github.com/ethyca/fides/pull/3188)
- Fixed unit tests for saas connector type endpoints now that we have >50 [#3101](https://github.com/ethyca/fides/pull/3101)
- Fixed nox docs link [#3121](https://github.com/ethyca/fides/pull/3121/files)

### Developer Experience

- Update fides deploy to use a new database.load_samples setting to initialize sample Systems, Datasets, and Connections for testing [#3102](https://github.com/ethyca/fides/pull/3102)
- Remove support for automatically configuring messaging (Mailgun) & storage (S3) using `.env` with `nox -s "fides_env(test)"` [#3102](https://github.com/ethyca/fides/pull/3102)
- Add smoke tests for consent management [#3158](https://github.com/ethyca/fides/pull/3158)
- Added nox command that opens dev docs [#3082](https://github.com/ethyca/fides/pull/3082)

## [2.11.0](https://github.com/ethyca/fides/compare/2.10.0...2.11.0)

### Added

- Access support for Shippo [#2484](https://github.com/ethyca/fides/pull/2484)
- Feature flags can be set such that they cannot be modified by the user [#2966](https://github.com/ethyca/fides/pull/2966)
- Added the datamap UI to make it open source [#2988](https://github.com/ethyca/fides/pull/2988)
- Introduced a `FixedLayout` component (from the datamap UI) for pages that need to be a fixed height and scroll within [#2992](https://github.com/ethyca/fides/pull/2992)
- Added preliminary privacy notice page [#2995](https://github.com/ethyca/fides/pull/2995)
- Table for privacy notices [#3001](https://github.com/ethyca/fides/pull/3001)
- Added connector template endpoint [#2946](https://github.com/ethyca/fides/pull/2946)
- Query params on connection type endpoint to filter by supported action type [#2996](https://github.com/ethyca/fides/pull/2996)
- Scope restrictions for privacy notice table in the UI [#3007](https://github.com/ethyca/fides/pull/3007)
- Toggle for enabling/disabling privacy notices in the UI [#3010](https://github.com/ethyca/fides/pull/3010)
- Add endpoint to retrieve privacy notices grouped by their associated data uses [#2956](https://github.com/ethyca/fides/pull/2956)
- Support for uploading custom connector templates via the UI [#2997](https://github.com/ethyca/fides/pull/2997)
- Add a backwards-compatible workflow for saving and propagating consent preferences with respect to Privacy Notices [#3016](https://github.com/ethyca/fides/pull/3016)
- Empty state for privacy notices [#3027](https://github.com/ethyca/fides/pull/3027)
- Added Data flow modal [#3008](https://github.com/ethyca/fides/pull/3008)
- Update datamap table export [#3038](https://github.com/ethyca/fides/pull/3038)
- Added more advanced privacy center styling [#2943](https://github.com/ethyca/fides/pull/2943)
- Backend privacy experiences foundation [#3146](https://github.com/ethyca/fides/pull/3146)

### Changed

- Set `privacyDeclarationDeprecatedFields` flags to false and set `userCannotModify` to true [2987](https://github.com/ethyca/fides/pull/2987)
- Restored `nav-config` back to the admin-ui [#2990](https://github.com/ethyca/fides/pull/2990)
- Bumped supported Python versions to 3.10.11, 3.9.16, and 3.8.14 [#2936](https://github.com/ethyca/fides/pull/2936)
- Modify privacy center default config to only request email identities, and add validation preventing requesting both email & phone identities [#2539](https://github.com/ethyca/fides/pull/2539)
- SaaS connector icons are now dynamically loaded from the connector templates [#3018](https://github.com/ethyca/fides/pull/3018)
- Updated consentmechanism Enum to rename "necessary" to "notice_only" [#3048](https://github.com/ethyca/fides/pull/3048)
- Updated test data for Mongo, CLI [#3011](https://github.com/ethyca/fides/pull/3011)
- Updated the check for if a user can assign owner roles to be scope-based instead of role-based [#2964](https://github.com/ethyca/fides/pull/2964)
- Replaced menu in user management table with delete icon [#2958](https://github.com/ethyca/fides/pull/2958)
- Added extra fields to webhook payloads [#2830](https://github.com/ethyca/fides/pull/2830)

### Removed

- Removed interzone navigation logic now that the datamap UI and admin UI are one app [#2990](https://github.com/ethyca/fides/pull/2990)
- Remove the `unknown` state for generated datasets displaying on fidesplus [#2957](https://github.com/ethyca/fides/pull/2957)
- Removed datamap export API [#2999](https://github.com/ethyca/fides/pull/2999)

### Developer Experience

- Nox commands for git tagging to support feature branch builds [#2979](https://github.com/ethyca/fides/pull/2979)
- Changed test environment (`nox -s fides_env`) to run `fides deploy` for local testing [#3071](https://github.com/ethyca/fides/pull/3017)
- Publish git-tag specific docker images [#3050](https://github.com/ethyca/fides/pull/3050)

## [2.10.0](https://github.com/ethyca/fides/compare/2.9.2...2.10.0)

### Added

- Allow users to configure their username and password via the config file [#2884](https://github.com/ethyca/fides/pull/2884)
- Add authentication to the `masking` endpoints as well as accompanying scopes [#2909](https://github.com/ethyca/fides/pull/2909)
- Add an Organization Management page (beta) [#2908](https://github.com/ethyca/fides/pull/2908)
- Adds assigned systems to user management table [#2922](https://github.com/ethyca/fides/pull/2922)
- APIs to support Privacy Notice management (create, read, update) [#2928](https://github.com/ethyca/fides/pull/2928)

### Changed

- Improved standard layout for large width screens and polished misc. pages [#2869](https://github.com/ethyca/fides/pull/2869)
- Changed UI paths in the admin-ui [#2869](https://github.com/ethyca/fides/pull/2892)
  - `/add-systems/new` --> `/add-systems/manual`
  - `/system` --> `/systems`
- Added individual ID routes for systems [#2902](https://github.com/ethyca/fides/pull/2902)
- Deprecated adding scopes to users directly; you can only add roles. [#2848](https://github.com/ethyca/fides/pull/2848/files)
- Changed About Fides page to say "Fides Core Version:" over "Version". [#2899](https://github.com/ethyca/fides/pull/2899)
- Polish Admin UI header & navigation [#2897](https://github.com/ethyca/fides/pull/2897)
- Give new users a "viewer" role by default [#2900](https://github.com/ethyca/fides/pull/2900)
- Tie together save states for user permissions and systems [#2913](https://github.com/ethyca/fides/pull/2913)
- Removing payment types from Stripe connector params [#2915](https://github.com/ethyca/fides/pull/2915)
- Viewer role can now access a restricted version of the user management page [#2933](https://github.com/ethyca/fides/pull/2933)
- Change Privacy Center email placeholder text [#2935](https://github.com/ethyca/fides/pull/2935)
- Restricted setting Approvers as System Managers [#2891](https://github.com/ethyca/fides/pull/2891)
- Adds confirmation modal when downgrading user to "approver" role via Admin UI [#2924](https://github.com/ethyca/fides/pull/2924)
- Changed the toast message for new users to include access control info [#2939](https://github.com/ethyca/fides/pull/2939)
- Add Data Stewards to datamap export [#2962](https://github.com/ethyca/fides/pull/2962)

### Fixed

- Restricted Contributors from being able to create Owners [#2888](https://github.com/ethyca/fides/pull/2888)
- Allow for dynamic aspect ratio for logo on Privacy Center 404 [#2895](https://github.com/ethyca/fides/pull/2895)
- Allow for dynamic aspect ratio for logo on consent page [#2895](https://github.com/ethyca/fides/pull/2895)
- Align role dscription drawer of Admin UI with top nav: [#2932](https://github.com/ethyca/fides/pull/2932)
- Fixed error message when a user is assigned to be an approver without any systems [#2953](https://github.com/ethyca/fides/pull/2953)

### Developer Experience

- Update frontend npm packages (admin-ui, privacy-center, cypress-e2e) [#2921](https://github.com/ethyca/fides/pull/2921)

## [2.9.2](https://github.com/ethyca/fides/compare/2.9.1...2.9.2)

### Fixed

- Allow multiple data uses as long as their processing activity name is different [#2905](https://github.com/ethyca/fides/pull/2905)
- use HTML property, not text, when dispatching Mailchimp Transactional emails [#2901](https://github.com/ethyca/fides/pull/2901)
- Remove policy key from Privacy Center submission modal [#2912](https://github.com/ethyca/fides/pull/2912)

## [2.9.1](https://github.com/ethyca/fides/compare/2.9.0...2.9.1)

### Added

- Added Attentive erasure email connector [#2782](https://github.com/ethyca/fides/pull/2782)

### Changed

- Removed dataset based email connectors [#2782](https://github.com/ethyca/fides/pull/2782)
- Changed Auth0's authentication strategy from `bearer` to `oauth2_client_credentials` [#2820](https://github.com/ethyca/fides/pull/2820)
- renamed the privacy declarations field "Privacy declaration name (deprecated)" to "Processing Activity" [#711](https://github.com/ethyca/fidesplus/issues/711)

### Fixed

- Fixed issue where the scopes list passed into FidesUserPermission could get mutated with the total_scopes call [#2883](https://github.com/ethyca/fides/pull/2883)

### Removed

- removed the `privacyDeclarationDeprecatedFields` flag [#711](https://github.com/ethyca/fidesplus/issues/711)

## [2.9.0](https://github.com/ethyca/fides/compare/2.8.3...2.9.0)

### Added

- The ability to assign users as system managers for a specific system [#2714](https://github.com/ethyca/fides/pull/2714)
- New endpoints to add and remove users as system managers [#2726](https://github.com/ethyca/fides/pull/2726)
- Warning about access control migration to the UI [#2842](https://github.com/ethyca/fides/pull/2842)
- Adds Role Assignment UI [#2739](https://github.com/ethyca/fides/pull/2739)
- Add an automated migration to give users a `viewer` role [#2821](https://github.com/ethyca/fides/pull/2821)

### Changed

- Removed "progressive" navigation that would hide Admin UI tabs until Systems / Connections were configured [#2762](https://github.com/ethyca/fides/pull/2762)
- Added `system.privacy_declaration.name` to datamap response [#2831](https://github.com/ethyca/fides/pull/2831/files)

### Developer Experience

- Retired legacy `navV2` feature flag [#2762](https://github.com/ethyca/fides/pull/2762)
- Update Admin UI Layout to fill viewport height [#2812](https://github.com/ethyca/fides/pull/2812)

### Fixed

- Fixed issue where unsaved changes warning would always show up when running fidesplus [#2788](https://github.com/ethyca/fides/issues/2788)
- Fixed problem in datamap export with datasets that had been updated via SaaS instantiation [#2841](https://github.com/ethyca/fides/pull/2841)
- Fixed problem in datamap export with inconsistent custom field ordering [#2859](https://github.com/ethyca/fides/pull/2859)

## [2.8.3](https://github.com/ethyca/fides/compare/2.8.2...2.8.3)

### Added

- Serialise `bson.ObjectId` types in SAR data packages [#2785](https://github.com/ethyca/fides/pull/2785)

### Fixed

- Fixed issue where more than 1 populated custom fields removed a system from the datamap export [#2825](https://github.com/ethyca/fides/pull/2825)

## [2.8.2](https://github.com/ethyca/fides/compare/2.8.1...2.8.2)

### Fixed

- Resolved a bug that stopped custom fields populating the visual datamap [#2775](https://github.com/ethyca/fides/pull/2775)
- Patch appconfig migration to handle existing db record [#2780](https://github.com/ethyca/fides/pull/2780)

## [2.8.1](https://github.com/ethyca/fides/compare/2.8.0...2.8.1)

### Fixed

- Disabled hiding Admin UI based on user scopes [#2771](https://github.com/ethyca/fides/pull/2771)

## [2.8.0](https://github.com/ethyca/fides/compare/2.7.1...2.8.0)

### Added

- Add API support for messaging config properties [#2551](https://github.com/ethyca/fides/pull/2551)
- Access and erasure support for Kustomer [#2520](https://github.com/ethyca/fides/pull/2520)
- Added the `erase_after` field on collections to be able to set the order for erasures [#2619](https://github.com/ethyca/fides/pull/2619)
- Add a toggle to filter the system classification to only return those with classification data [#2700](https://github.com/ethyca/fides/pull/2700)
- Added backend role-based permissions [#2671](https://github.com/ethyca/fides/pull/2671)
- Access and erasure for Vend SaaS Connector [#1869](https://github.com/ethyca/fides/issues/1869)
- Added endpoints for storage and messaging config setup status [#2690](https://github.com/ethyca/fides/pull/2690)
- Access and erasure for Jira SaaS Connector [#1871](https://github.com/ethyca/fides/issues/1871)
- Access and erasure support for Delighted [#2244](https://github.com/ethyca/fides/pull/2244)
- Improve "Upload a new dataset YAML" [#1531](https://github.com/ethyca/fides/pull/2258)
- Input validation and sanitization for Privacy Request fields [#2655](https://github.com/ethyca/fides/pull/2655)
- Access and erasure support for Yotpo [#2708](https://github.com/ethyca/fides/pull/2708)
- Custom Field Library Tab [#527](https://github.com/ethyca/fides/pull/2693)
- Allow SendGrid template usage [#2728](https://github.com/ethyca/fides/pull/2728)
- Added ConnectorRunner to simplify SaaS connector testing [#1795](https://github.com/ethyca/fides/pull/1795)
- Adds support for Mailchimp Transactional as a messaging config [#2742](https://github.com/ethyca/fides/pull/2742)

### Changed

- Admin UI
  - Add flow for selecting system types when manually creating a system [#2530](https://github.com/ethyca/fides/pull/2530)
  - Updated forms for privacy declarations [#2648](https://github.com/ethyca/fides/pull/2648)
  - Delete flow for privacy declarations [#2664](https://github.com/ethyca/fides/pull/2664)
  - Add framework to have UI elements respect the user's scopes [#2682](https://github.com/ethyca/fides/pull/2682)
  - "Manual Webhook" has been renamed to "Manual Process". [#2717](https://github.com/ethyca/fides/pull/2717)
- Convert all config values to Pydantic `Field` objects [#2613](https://github.com/ethyca/fides/pull/2613)
- Add warning to 'fides deploy' when installed outside of a virtual environment [#2641](https://github.com/ethyca/fides/pull/2641)
- Redesigned the default/init config file to be auto-documented. Also updates the `fides init` logic and analytics consent logic [#2694](https://github.com/ethyca/fides/pull/2694)
- Change how config creation/import is handled across the application [#2622](https://github.com/ethyca/fides/pull/2622)
- Update the CLI aesthetics & docstrings [#2703](https://github.com/ethyca/fides/pull/2703)
- Updates Roles->Scopes Mapping [#2744](https://github.com/ethyca/fides/pull/2744)
- Return user scopes as an enum, as well as total scopes [#2741](https://github.com/ethyca/fides/pull/2741)
- Update `MessagingServiceType` enum to be lowercased throughout [#2746](https://github.com/ethyca/fides/pull/2746)

### Developer Experience

- Set the security environment of the fides dev setup to `prod` instead of `dev` [#2588](https://github.com/ethyca/fides/pull/2588)
- Removed unexpected default Redis password [#2666](https://github.com/ethyca/fides/pull/2666)
- Privacy Center
  - Typechecking and validation of the `config.json` will be checked for backwards-compatibility. [#2661](https://github.com/ethyca/fides/pull/2661)
- Combined conftest.py files [#2669](https://github.com/ethyca/fides/pull/2669)

### Fixed

- Fix support for "redis.user" setting when authenticating to the Redis cache [#2666](https://github.com/ethyca/fides/pull/2666)
- Fix error with the classify dataset feature flag not writing the dataset to the server [#2675](https://github.com/ethyca/fides/pull/2675)
- Allow string dates to stay strings in cache decoding [#2695](https://github.com/ethyca/fides/pull/2695)
- Admin UI
  - Remove Identifiability (Data Qualifier) from taxonomy editor [2684](https://github.com/ethyca/fides/pull/2684)
- FE: Custom field selections binding issue on Taxonomy tabs [#2659](https://github.com/ethyca/fides/pull/2693/)
- Fix Privacy Request Status when submitting a consent request when identity verification is required [#2736](https://github.com/ethyca/fides/pull/2736)

## [2.7.1](https://github.com/ethyca/fides/compare/2.7.0...2.7.1)

- Fix error with the classify dataset feature flag not writing the dataset to the server [#2675](https://github.com/ethyca/fides/pull/2675)

## [2.7.0](https://github.com/ethyca/fides/compare/2.6.6...2.7.0)

- Fides API

  - Access and erasure support for Braintree [#2223](https://github.com/ethyca/fides/pull/2223)
  - Added route to send a test message [#2585](https://github.com/ethyca/fides/pull/2585)
  - Add default storage configuration functionality and associated APIs [#2438](https://github.com/ethyca/fides/pull/2438)

- Admin UI

  - Custom Metadata [#2536](https://github.com/ethyca/fides/pull/2536)
    - Create Custom Lists
    - Create Custom Field Definition
    - Create custom fields from a the taxonomy editor
    - Provide a custom field value in a resource
    - Bulk edit custom field values [#2612](https://github.com/ethyca/fides/issues/2612)
    - Custom metadata UI Polish [#2624](https://github.com/ethyca/fides/pull/2625)

- Privacy Center

  - The consent config default value can depend on whether Global Privacy Control is enabled. [#2341](https://github.com/ethyca/fides/pull/2341)
  - When GPC is enabled, the UI indicates which data uses are opted out by default. [#2596](https://github.com/ethyca/fides/pull/2596)
  - `inspectForBrowserIdentities` now also looks for `ljt_readerID`. [#2543](https://github.com/ethyca/fides/pull/2543)

### Added

- Added new Wunderkind Consent Saas Connector [#2600](https://github.com/ethyca/fides/pull/2600)
- Added new Sovrn Email Consent Connector [#2543](https://github.com/ethyca/fides/pull/2543/)
- Log Fides version at startup [#2566](https://github.com/ethyca/fides/pull/2566)

### Changed

- Update Admin UI to show all action types (access, erasure, consent, update) [#2523](https://github.com/ethyca/fides/pull/2523)
- Removes legacy `verify_oauth_client` function [#2527](https://github.com/ethyca/fides/pull/2527)
- Updated the UI for adding systems to a new design [#2490](https://github.com/ethyca/fides/pull/2490)
- Minor logging improvements [#2566](https://github.com/ethyca/fides/pull/2566)
- Various form components now take a `stacked` or `inline` variant [#2542](https://github.com/ethyca/fides/pull/2542)
- UX fixes for user management [#2537](https://github.com/ethyca/fides/pull/2537)
- Updating Firebase Auth connector to mask the user with a delete instead of an update [#2602](https://github.com/ethyca/fides/pull/2602)

### Fixed

- Fixed bug where refreshing a page in the UI would result in a 404 [#2502](https://github.com/ethyca/fides/pull/2502)
- Usernames are case insensitive now and prevent all duplicates [#2487](https://github.com/ethyca/fides/pull/2487)
  - This PR contains a migration that deletes duplicate users and keeps the oldest original account.
- Update Logos for shipped connectors [#2464](https://github.com/ethyca/fides/pull/2587)
- Search field on privacy request page isn't working [#2270](https://github.com/ethyca/fides/pull/2595)
- Fix connection dropdown in integration table to not be disabled add system creation [#3589](https://github.com/ethyca/fides/pull/3589)

### Developer Experience

- Added new Cypress E2E smoke tests [#2241](https://github.com/ethyca/fides/pull/2241)
- New command `nox -s e2e_test` which will spin up the test environment and run true E2E Cypress tests against it [#2417](https://github.com/ethyca/fides/pull/2417)
- Cypress E2E tests now run in CI and are reported to Cypress Cloud [#2417](https://github.com/ethyca/fides/pull/2417)
- Change from `randomint` to `uuid` in mongodb tests to reduce flakiness. [#2591](https://github.com/ethyca/fides/pull/2591)

### Removed

- Remove feature flagged config wizard stepper from Admin UI [#2553](https://github.com/ethyca/fides/pull/2553)

## [2.6.6](https://github.com/ethyca/fides/compare/2.6.5...2.6.6)

### Changed

- Improve Readability for Custom Masking Override Exceptions [#2593](https://github.com/ethyca/fides/pull/2593)

## [2.6.5](https://github.com/ethyca/fides/compare/2.6.4...2.6.5)

### Added

- Added config properties to override database Engine parameters [#2511](https://github.com/ethyca/fides/pull/2511)
- Increased default pool_size and max_overflow to 50 [#2560](https://github.com/ethyca/fides/pull/2560)

## [2.6.4](https://github.com/ethyca/fides/compare/2.6.3...2.6.4)

### Fixed

- Fixed bug for SMS completion notification not being sent [#2526](https://github.com/ethyca/fides/issues/2526)
- Fixed bug where refreshing a page in the UI would result in a 404 [#2502](https://github.com/ethyca/fides/pull/2502)

## [2.6.3](https://github.com/ethyca/fides/compare/2.6.2...2.6.3)

### Fixed

- Handle case where legacy dataset has meta: null [#2524](https://github.com/ethyca/fides/pull/2524)

## [2.6.2](https://github.com/ethyca/fides/compare/2.6.1...2.6.2)

### Fixed

- Issue addressing missing field in dataset migration [#2510](https://github.com/ethyca/fides/pull/2510)

## [2.6.1](https://github.com/ethyca/fides/compare/2.6.0...2.6.1)

### Fixed

- Fix errors when privacy requests execute concurrently without workers [#2489](https://github.com/ethyca/fides/pull/2489)
- Enable saas request overrides to run in worker runtime [#2489](https://github.com/ethyca/fides/pull/2489)

## [2.6.0](https://github.com/ethyca/fides/compare/2.5.1...2.6.0)

### Added

- Added the `env` option to the `security` configuration options to allow for users to completely secure the API endpoints [#2267](https://github.com/ethyca/fides/pull/2267)
- Unified Fides Resources
  - Added a dataset dropdown selector when configuring a connector to link an existing dataset to the connector configuration. [#2162](https://github.com/ethyca/fides/pull/2162)
  - Added new datasetconfig.ctl_dataset_id field to unify fides dataset resources [#2046](https://github.com/ethyca/fides/pull/2046)
- Add new connection config routes that couple them with systems [#2249](https://github.com/ethyca/fides/pull/2249)
- Add new select/deselect all permissions buttons [#2437](https://github.com/ethyca/fides/pull/2437)
- Endpoints to allow a user with the `user:password-reset` scope to reset users' passwords. In addition, users no longer require a scope to edit their own passwords. [#2373](https://github.com/ethyca/fides/pull/2373)
- New form to reset a user's password without knowing an old password [#2390](https://github.com/ethyca/fides/pull/2390)
- Approve & deny buttons on the "Request details" page. [#2473](https://github.com/ethyca/fides/pull/2473)
- Consent Propagation
  - Add the ability to execute Consent Requests via the Privacy Request Execution layer [#2125](https://github.com/ethyca/fides/pull/2125)
  - Add a Mailchimp Transactional Consent Connector [#2194](https://github.com/ethyca/fides/pull/2194)
  - Allow defining a list of opt-in and/or opt-out requests in consent connectors [#2315](https://github.com/ethyca/fides/pull/2315)
  - Add a Google Analytics Consent Connector for GA4 properties [#2302](https://github.com/ethyca/fides/pull/2302)
  - Pass the GA Cookie from the Privacy Center [#2337](https://github.com/ethyca/fides/pull/2337)
  - Rename "user_id" to more specific "ga_client_id" [#2356](https://github.com/ethyca/fides/pull/2356)
  - Patch Google Analytics Consent Connector to delete by client_id [#2355](https://github.com/ethyca/fides/pull/2355)
  - Add a "skip_param_values option" to optionally skip when we are missing param values in the body [#2384](https://github.com/ethyca/fides/pull/2384)
  - Adds a new Universal Analytics Connector that works with the UA Tracking Id
- Adds intake and storage of Global Privacy Control Signal props for Consent [#2599](https://github.com/ethyca/fides/pull/2599)

### Changed

- Unified Fides Resources
  - Removed several fidesops schemas for DSR's in favor of updated Fideslang schemas [#2009](https://github.com/ethyca/fides/pull/2009)
  - Removed DatasetConfig.dataset field [#2096](https://github.com/ethyca/fides/pull/2096)
  - Updated UI dataset config routes to use new unified routes [#2113](https://github.com/ethyca/fides/pull/2113)
  - Validate request body on crud endpoints on upsert. Validate dataset data categories before save. [#2134](https://github.com/ethyca/fides/pull/2134/)
  - Updated test env setup and quickstart to use new endpoints [#2225](https://github.com/ethyca/fides/pull/2225)
- Consent Propagation
  - Privacy Center consent options can now be marked as `executable` in order to propagate consent requests [#2193](https://github.com/ethyca/fides/pull/2193)
  - Add support for passing browser identities to consent request patches [#2304](https://github.com/ethyca/fides/pull/2304)
- Update fideslang to 1.3.3 [#2343](https://github.com/ethyca/fides/pull/2343)
- Display the request type instead of the policy name on the request table [#2382](https://github.com/ethyca/fides/pull/2382)
- Make denial reasons required [#2400](https://github.com/ethyca/fides/pull/2400)
- Display the policy key on the request details page [#2395](https://github.com/ethyca/fides/pull/2395)
- Updated CSV export [#2452](https://github.com/ethyca/fides/pull/2452)
- Privacy Request approval now uses a modal [#2443](https://github.com/ethyca/fides/pull/2443)

### Developer Experience

- `nox -s test_env` has been replaced with `nox -s "fides_env(dev)"`
- New command `nox -s "fides_env(test)"` creates a complete test environment with seed data (similar to `fides_env(dev)`) but with the production fides image so the built UI can be accessed at `localhost:8080` [#2399](https://github.com/ethyca/fides/pull/2399)
- Change from code climate to codecov for coverage reporting [#2402](https://github.com/ethyca/fides/pull/2402)

### Fixed

- Home screen header scaling and responsiveness issues [#2200](https://github.com/ethyca/fides/pull/2277)
- Privacy Center identity inputs validate even when they are optional. [#2308](https://github.com/ethyca/fides/pull/2308)
- The PII toggle defaults to false and PII will be hidden on page load [#2388](https://github.com/ethyca/fides/pull/2388)
- Fixed a CI bug caused by git security upgrades [#2441](https://github.com/ethyca/fides/pull/2441)
- Privacy Center
  - Identity inputs validate even when they are optional. [#2308](https://github.com/ethyca/fides/pull/2308)
  - Submit buttons show loading state and disable while submitting. [#2401](https://github.com/ethyca/fides/pull/2401)
  - Phone inputs no longer request country SVGs from external domain. [#2378](https://github.com/ethyca/fides/pull/2378)
  - Input validation errors no longer change the height of modals. [#2379](https://github.com/ethyca/fides/pull/2379)
- Patch masking strategies to better handle null and non-string inputs [#2307](https://github.com/ethyca/fides/pull/2377)
- Renamed prod pushes tag to be `latest` for privacy center and sample app [#2401](https://github.com/ethyca/fides/pull/2407)
- Update firebase connector to better handle non-existent users [#2439](https://github.com/ethyca/fides/pull/2439)

## [2.5.1](https://github.com/ethyca/fides/compare/2.5.0...2.5.1)

### Developer Experience

- Allow db resets only if `config.dev_mode` is `True` [#2321](https://github.com/ethyca/fides/pull/2321)

### Fixed

- Added a feature flag for the recent dataset classification UX changes [#2335](https://github.com/ethyca/fides/pull/2335)

### Security

- Add a check to the catchall path to prevent returning paths outside of the UI directory [#2330](https://github.com/ethyca/fides/pull/2330)

### Developer Experience

- Reduce size of local Docker images by fixing `.dockerignore` patterns [#2360](https://github.com/ethyca/fides/pull/2360)

## [2.5.0](https://github.com/ethyca/fides/compare/2.4.0...2.5.0)

### Docs

- Update the docs landing page and remove redundant docs [#2184](https://github.com/ethyca/fides/pull/2184)

### Added

- Added the `user` command group to the CLI. [#2153](https://github.com/ethyca/fides/pull/2153)
- Added `Code Climate` test coverage uploads. [#2198](https://github.com/ethyca/fides/pull/2198)
- Added the connection key to the execution log [#2100](https://github.com/ethyca/fides/pull/2100)
- Added endpoints to retrieve DSR `Rule`s and `Rule Target`s [#2116](https://github.com/ethyca/fides/pull/2116)
- Added Fides version number to account dropdown in the UI [#2140](https://github.com/ethyca/fides/pull/2140)
- Add link to Classify Systems page in nav side bar [#2128](https://github.com/ethyca/fides/pull/2128)
- Dataset classification UI now polls for results [#2123](https://github.com/ethyca/fides/pull/2123)
- Update Privacy Center Icons [#1800](https://github.com/ethyca/fides/pull/2139)
- Privacy Center `fides-consent.js`:
  - `Fides.shopify` integration function. [#2152](https://github.com/ethyca/fides/pull/2152)
  - Dedicated folder for integrations.
  - `Fides.meta` integration function (fbq). [#2217](https://github.com/ethyca/fides/pull/2217)
- Adds support for Twilio email service (Sendgrid) [#2154](https://github.com/ethyca/fides/pull/2154)
- Access and erasure support for Recharge [#1709](https://github.com/ethyca/fides/pull/1709)
- Access and erasure support for Friendbuy Nextgen [#2085](https://github.com/ethyca/fides/pull/2085)

### Changed

- Admin UI Feature Flags - [#2101](https://github.com/ethyca/fides/pull/2101)
  - Overrides can be saved in the browser.
  - Use `NEXT_PUBLIC_APP_ENV` for app-specific environment config.
  - No longer use `react-feature-flags` library.
  - Can have descriptions. [#2243](https://github.com/ethyca/fides/pull/2243)
- Made privacy declarations optional when adding systems manually - [#2173](https://github.com/ethyca/fides/pull/2173)
- Removed an unclear logging message. [#2266](https://github.com/ethyca/fides/pull/2266)
- Allow any user with `user:delete` scope to delete other users [#2148](https://github.com/ethyca/fides/pull/2148)
- Dynamic imports of custom overrides and SaaS test fixtures [#2169](https://github.com/ethyca/fides/pull/2169)
- Added `AuthenticatedClient` to custom request override interface [#2171](https://github.com/ethyca/fides/pull/2171)
- Only approve the specific collection instead of the entire dataset, display only top 1 classification by default [#2226](https://github.com/ethyca/fides/pull/2226)
- Update sample project resources for `fides evaluate` usage in `fides deploy` [#2253](https://github.com/ethyca/fides/pull/2253)

### Removed

- Removed unused object_name field on s3 storage config [#2133](https://github.com/ethyca/fides/pull/2133)

### Fixed

- Remove next-auth from privacy center to fix JS console error [#2090](https://github.com/ethyca/fides/pull/2090)
- Admin UI - Added Missing ability to assign `user:delete` in the permissions checkboxes [#2148](https://github.com/ethyca/fides/pull/2148)
- Nav bug: clicking on Privacy Request breadcrumb takes me to Home instead of /privacy-requests [#497](https://github.com/ethyca/fides/pull/2141)
- Side nav disappears when viewing request details [#2129](https://github.com/ethyca/fides/pull/2155)
- Remove usage of load dataset button and other dataset UI modifications [#2149](https://github.com/ethyca/fides/pull/2149)
- Improve readability for exceptions raised from custom request overrides [#2157](https://github.com/ethyca/fides/pull/2157)
- Importing custom request overrides on server startup [#2186](https://github.com/ethyca/fides/pull/2186)
- Remove warning when env vars default to blank strings in docker-compose [#2188](https://github.com/ethyca/fides/pull/2188)
- Fix Cookie House purchase modal flashing 'Error' in title [#2274](https://github.com/ethyca/fides/pull/2274)
- Stop dependency from upgrading `packaging` to version with known issue [#2273](https://github.com/ethyca/fides/pull/2273)
- Privacy center config no longer requires `identity_inputs` and will use `email` as a default [#2263](https://github.com/ethyca/fides/pull/2263)
- No longer display remaining days for privacy requests in terminal states [#2292](https://github.com/ethyca/fides/pull/2292)

### Removed

- Remove "Create New System" button when viewing systems. All systems can now be created via the "Add systems" button on the home page. [#2132](https://github.com/ethyca/fides/pull/2132)

## [2.4.0](https://github.com/ethyca/fides/compare/2.3.1...2.4.0)

### Developer Experience

- Include a pre-check workflow that collects the pytest suite [#2098](https://github.com/ethyca/fides/pull/2098)
- Write to the application db when running the app locally. Write to the test db when running pytest [#1731](https://github.com/ethyca/fides/pull/1731)

### Changed

- Move the `fides.ctl.core.` and `fides.ctl.connectors` modules into `fides.core` and `fides.connectors` respectively [#2097](https://github.com/ethyca/fides/pull/2097)
- Fides: Skip cypress tests due to nav bar 2.0 [#2102](https://github.com/ethyca/fides/pull/2103)

### Added

- Adds new erasure policy for complete user data masking [#1839](https://github.com/ethyca/fides/pull/1839)
- New Fides Home page [#1864](https://github.com/ethyca/fides/pull/2050)
- Nav 2.0 - Replace form flow side navs with top tabs [#2037](https://github.com/ethyca/fides/pull/2050)
- Adds new erasure policy for complete user data masking [#1839](https://github.com/ethyca/fides/pull/1839)
- Added ability to use Mailgun templates when sending emails. [#2039](https://github.com/ethyca/fides/pull/2039)
- Adds SMS id verification for consent [#2094](https://github.com/ethyca/fides/pull/2094)

### Fixed

- Store `fides_consent` cookie on the root domain of the Privacy Center [#2071](https://github.com/ethyca/fides/pull/2071)
- Properly set the expire-time for verification codes [#2105](https://github.com/ethyca/fides/pull/2105)

## [2.3.1](https://github.com/ethyca/fides/compare/2.3.0...2.3.1)

### Fixed

- Resolved an issue where the root_user was not being created [#2082](https://github.com/ethyca/fides/pull/2082)

### Added

- Nav redesign with sidebar groups. Feature flagged to only be visible in dev mode until release. [#2030](https://github.com/ethyca/fides/pull/2047)
- Improved error handling for incorrect app encryption key [#2089](https://github.com/ethyca/fides/pull/2089)
- Access and erasure support for Friendbuy API [#2019](https://github.com/ethyca/fides/pull/2019)

## [2.3.0](https://github.com/ethyca/fides/compare/2.2.2...2.3.0)

### Added

- Common Subscriptions for app-wide data and feature checks. [#2030](https://github.com/ethyca/fides/pull/2030)
- Send email alerts on privacy request failures once the specified threshold is reached. [#1793](https://github.com/ethyca/fides/pull/1793)
- DSR Notifications (toast) [#1895](https://github.com/ethyca/fides/pull/1895)
- DSR configure alerts btn [#1895](https://github.com/ethyca/fides/pull/1895)
- DSR configure alters (FE) [#1895](https://github.com/ethyca/fides/pull/1895)
- Add a `usage` session to Nox to print full session docstrings. [#2022](https://github.com/ethyca/fides/pull/2022)

### Added

- Adds notifications section to toml files [#2026](https://github.com/ethyca/fides/pull/2060)

### Changed

- Updated to use `loguru` logging library throughout codebase [#2031](https://github.com/ethyca/fides/pull/2031)
- Do not always create a `fides.toml` by default [#2023](https://github.com/ethyca/fides/pull/2023)
- The `fideslib` module has been merged into `fides`, code redundancies have been removed [#1859](https://github.com/ethyca/fides/pull/1859)
- Replace 'ingress' and 'egress' with 'sources' and 'destinations' across UI [#2044](https://github.com/ethyca/fides/pull/2044)
- Update the functionality of `fides pull -a <filename>` to include _all_ resource types. [#2083](https://github.com/ethyca/fides/pull/2083)

### Fixed

- Timing issues with bulk DSR reprocessing, specifically when analytics are enabled [#2015](https://github.com/ethyca/fides/pull/2015)
- Error caused by running erasure requests with disabled connectors [#2045](https://github.com/ethyca/fides/pull/2045)
- Changes the SlowAPI ratelimiter's backend to use memory instead of Redis [#2054](https://github.com/ethyca/fides/pull/2058)

## [2.2.2](https://github.com/ethyca/fides/compare/2.2.1...2.2.2)

### Docs

- Updated the readme to use new new [docs site](http://docs.ethyca.com) [#2020](https://github.com/ethyca/fides/pull/2020)

### Deprecated

- The documentation site hosted in the `/docs` directory has been deprecated. All documentation updates will be hosted at the new [docs site](http://docs.ethyca.com) [#2020](https://github.com/ethyca/fides/pull/2020)

### Fixed

- Fixed mypy and pylint errors [#2013](https://github.com/ethyca/fides/pull/2013)
- Update connection test endpoint to be effectively non-blocking [#2000](https://github.com/ethyca/fides/pull/2000)
- Update Fides connector to better handle children with no access results [#2012](https://github.com/ethyca/fides/pull/2012)

## [2.2.1](https://github.com/ethyca/fides/compare/2.2.0...2.2.1)

### Added

- Add health check indicator for data flow scanning option [#1973](https://github.com/ethyca/fides/pull/1973)

### Changed

- The `celery.toml` is no longer used, instead it is a subsection of the `fides.toml` file [#1990](https://github.com/ethyca/fides/pull/1990)
- Update sample project landing page copy to be version-agnostic [#1958](https://github.com/ethyca/fides/pull/1958)
- `get` and `ls` CLI commands now return valid `fides` object YAML [#1991](https://github.com/ethyca/fides/pull/1991)

### Developer Experience

- Remove duplicate fastapi-caching and pin version. [#1765](https://github.com/ethyca/fides/pull/1765)

## [2.2.0](https://github.com/ethyca/fides/compare/2.1.0...2.2.0)

### Added

- Send email alerts on privacy request failures once the specified threshold is reached. [#1793](https://github.com/ethyca/fides/pull/1793)
- Add authenticated privacy request route. [#1819](https://github.com/ethyca/fides/pull/1819)
- Enable the onboarding flow [#1836](https://github.com/ethyca/fides/pull/1836)
- Access and erasure support for Fullstory API [#1821](https://github.com/ethyca/fides/pull/1821)
- Add function to poll privacy request for completion [#1860](https://github.com/ethyca/fides/pull/1860)
- Added rescan flow for the data flow scanner [#1844](https://github.com/ethyca/fides/pull/1844)
- Add rescan flow for the data flow scanner [#1844](https://github.com/ethyca/fides/pull/1844)
- Add Fides connector to support parent-child Fides deployments [#1861](https://github.com/ethyca/fides/pull/1861)
- Classification UI now polls for updates to classifications [#1908](https://github.com/ethyca/fides/pull/1908)

### Changed

- The organization info form step is now skipped if the server already has organization info. [#1840](https://github.com/ethyca/fides/pull/1840)
- Removed the description column from the classify systems page. [#1867](https://github.com/ethyca/fides/pull/1867)
- Retrieve child results during fides connector execution [#1967](https://github.com/ethyca/fides/pull/1967)

### Fixed

- Fix error in parent user creation seeding. [#1832](https://github.com/ethyca/fides/issues/1832)
- Fix DSR error due to unfiltered empty identities [#1901](https://github.com/ethyca/fides/pull/1907)

### Docs

- Remove documentation about no-longer used connection string override [#1824](https://github.com/ethyca/fides/pull/1824)
- Fix typo in headings [#1824](https://github.com/ethyca/fides/pull/1824)
- Update documentation to reflect configs necessary for mailgun, twilio_sms and twilio_email service types [#1846](https://github.com/ethyca/fides/pull/1846)

...

## [2.1.0](https://github.com/ethyca/fides/compare/2.0.0...2.1.0)

### Added

- Classification flow for system data flows
- Classification is now triggered as part of data flow scanning
- Include `ingress` and `egress` fields on system export and `datamap/` endpoint [#1740](https://github.com/ethyca/fides/pull/1740)
- Repeatable unique identifier for dataset fides_keys and metadata [#1786](https://github.com/ethyca/fides/pull/1786)
- Adds SMS support for identity verification notifications [#1726](https://github.com/ethyca/fides/pull/1726)
- Added phone number validation in back-end and react phone number form in Privacy Center [#1745](https://github.com/ethyca/fides/pull/1745)
- Adds SMS message template for all subject notifications [#1743](https://github.com/ethyca/fides/pull/1743)
- Privacy-Center-Cypress workflow for CI checks of the Privacy Center. [#1722](https://github.com/ethyca/fides/pull/1722)
- Privacy Center `fides-consent.js` script for accessing consent on external pages. [Details](/clients/privacy-center/packages/fides-consent/README.md)
- Erasure support for Twilio Conversations API [#1673](https://github.com/ethyca/fides/pull/1673)
- Webserver port can now be configured via the CLI command [#1858](https://github.com/ethyca/fides/pull/1858)

### Changed

- Optional dependencies are no longer used for 3rd-party connectivity. Instead they are used to isolate dangerous dependencies. [#1679](https://github.com/ethyca/fides/pull/1679)
- All Next pages now automatically require login. [#1670](https://github.com/ethyca/fides/pull/1670)
- Running the `webserver` command no longer prompts the user to opt out/in to analytics[#1724](https://github.com/ethyca/fides/pull/1724)

### Developer Experience

- Admin-UI-Cypress tests that fail in CI will now upload screen recordings for debugging. [#1728](https://github.com/ethyca/fides/pull/1728/files/c23e62fea284f7910028c8483feff893903068b8#r1019491323)
- Enable remote debugging from VSCode of live dev app [#1780](https://github.com/ethyca/fides/pull/1780)

### Removed

- Removed the Privacy Center `cookieName` config introduced in 2.0.0. [#1756](https://github.com/ethyca/fides/pull/1756)

### Fixed

- Exceptions are no longer raised when sending analytics on Windows [#1666](https://github.com/ethyca/fides/pull/1666)
- Fixed wording on identity verification modal in the Privacy Center [#1674](https://github.com/ethyca/fides/pull/1674)
- Update system fides_key tooltip text [#1533](https://github.com/ethyca/fides/pull/1685)
- Removed local storage parsing that is redundant with redux-persist. [#1678](https://github.com/ethyca/fides/pull/1678)
- Show a helpful error message if Docker daemon is not running during "fides deploy" [#1694](https://github.com/ethyca/fides/pull/1694)
- Allow users to query their own permissions, including root user. [#1698](https://github.com/ethyca/fides/pull/1698)
- Single-select taxonomy fields legal basis and special category can be cleared. [#1712](https://github.com/ethyca/fides/pull/1712)
- Fixes the issue where the security config is not properly loading from environment variables. [#1718](https://github.com/ethyca/fides/pull/1718)
- Fixes the issue where the CLI can't run without the config values required by the webserver. [#1811](https://github.com/ethyca/fides/pull/1811)
- Correctly handle response from adobe jwt auth endpoint as milliseconds, rather than seconds. [#1754](https://github.com/ethyca/fides/pull/1754)
- Fixed styling issues with the `EditDrawer` component. [#1803](https://github.com/ethyca/fides/pull/1803)

### Security

- Bumped versions of packages that use OpenSSL [#1683](https://github.com/ethyca/fides/pull/1683)

## [2.0.0](https://github.com/ethyca/fides/compare/1.9.6...2.0.0)

### Added

- Allow delete-only SaaS connector endpoints [#1200](https://github.com/ethyca/fides/pull/1200)
- Privacy center consent choices store a browser cookie. [#1364](https://github.com/ethyca/fides/pull/1364)
  - The format is generic. A reasonable set of defaults will be added later: [#1444](https://github.com/ethyca/fides/issues/1444)
  - The cookie name defaults to `fides_consent` but can be configured under `config.json > consent > cookieName`.
  - Each consent option can provide an array of `cookieKeys`.
- Individually select and reprocess DSRs that have errored [#1203](https://github.com/ethyca/fides/pull/1489)
- Bulk select and reprocess DSRs that have errored [#1205](https://github.com/ethyca/fides/pull/1489)
- Config Wizard: AWS scan results populate in system review forms. [#1454](https://github.com/ethyca/fides/pull/1454)
- Integrate rate limiter with Saas Connectors. [#1433](https://github.com/ethyca/fides/pull/1433)
- Config Wizard: Added a column selector to the scan results page of the config wizard [#1590](https://github.com/ethyca/fides/pull/1590)
- Config Wizard: Flow for runtime scanner option [#1640](https://github.com/ethyca/fides/pull/1640)
- Access support for Twilio Conversations API [#1520](https://github.com/ethyca/fides/pull/1520)
- Message Config: Adds Twilio Email/SMS support [#1519](https://github.com/ethyca/fides/pull/1519)

### Changed

- Updated mypy to version 0.981 and Python to version 3.10.7 [#1448](https://github.com/ethyca/fides/pull/1448)

### Developer Experience

- Repository dispatch events are sent to fidesctl-plus and fidesops-plus [#1263](https://github.com/ethyca/fides/pull/1263)
- Only the `docs-authors` team members are specified as `CODEOWNERS` [#1446](https://github.com/ethyca/fides/pull/1446)
- Updates the default local configuration to not defer tasks to a worker node [#1552](https://github.com/ethyca/fides/pull/1552/)
- Updates the healthcheck to return health status of connected Celery workers [#1588](https://github.com/ethyca/fides/pull/1588)

### Docs

- Remove the tutorial to prepare for new update [#1543](https://github.com/ethyca/fides/pull/1543)
- Add system management via UI documentation [#1541](https://github.com/ethyca/fides/pull/1541)
- Added DSR quickstart docs, restructured docs navigation [#1651](https://github.com/ethyca/fides/pull/1651)
- Update privacy request execution overview docs [#1258](https://github.com/ethyca/fides/pull/1490)

### Fixed

- Fixed system dependencies appearing as "N/A" in the datamap endpoint when there are no privacy declarations [#1649](https://github.com/ethyca/fides/pull/1649)

## [1.9.6](https://github.com/ethyca/fides/compare/1.9.5...1.9.6)

### Fixed

- Include systems without a privacy declaration on data map [#1603](https://github.com/ethyca/fides/pull/1603)
- Handle malformed tokens [#1523](https://github.com/ethyca/fides/pull/1523)
- Remove thrown exception from getAllPrivacyRequests method [#1592](https://github.com/ethyca/fides/pull/1593)
- Include systems without a privacy declaration on data map [#1603](https://github.com/ethyca/fides/pull/1603)
- After editing a dataset, the table will stay on the previously selected collection instead of resetting to the first one. [#1511](https://github.com/ethyca/fides/pull/1511)
- Fix redis `db_index` config issue [#1647](https://github.com/ethyca/fides/pull/1647)

### Docs

- Add unlinked docs and fix any remaining broken links [#1266](https://github.com/ethyca/fides/pull/1266)
- Update privacy center docs to include consent information [#1537](https://github.com/ethyca/fides/pull/1537)
- Update UI docs to include DSR countdown information and additional descriptions/filtering [#1545](https://github.com/ethyca/fides/pull/1545)

### Changed

- Allow multiple masking strategies to be specified when using fides as a masking engine [#1647](https://github.com/ethyca/fides/pull/1647)

## [1.9.5](https://github.com/ethyca/fides/compare/1.9.4...1.9.5)

### Added

- The database includes a `plus_system_scans` relation, to track the status and results of System Scanner executions in fidesctl-plus [#1554](https://github.com/ethyca/fides/pull/1554)

## [1.9.4](https://github.com/ethyca/fides/compare/1.9.2...1.9.4)

### Fixed

- After editing a dataset, the table will stay on the previously selected collection instead of resetting to the first one. [#1511](https://github.com/ethyca/fides/pull/1511)

## [1.9.2](https://github.com/ethyca/fides/compare/1.9.1...1.9.2)

### Deprecated

- Added a deprecation warning for the entire package [#1244](https://github.com/ethyca/fides/pull/1244)

### Added

- Dataset generation enhancements using Fides Classify for Plus users:

  - Integrate Fides Plus API into placeholder features introduced in 1.9.0. [#1194](https://github.com/ethyca/fides/pull/1194)

- Fides Admin UI:

  - Configure Connector after creation [#1204](https://github.com/ethyca/fides/pull/1356)

### Fixed

- Privacy Center:
  - Handle error on startup if server isn't running [#1239](https://github.com/ethyca/fides/pull/1239)
  - Fix styling issue with cards [#1240](https://github.com/ethyca/fides/pull/1240)
  - Redirect to index on consent save [#1238](https://github.com/ethyca/fides/pull/1238)

## [1.9.1](https://github.com/ethyca/fides/compare/1.9.0...1.9.1)

### Changed

- Update fideslang to v1.3.1 [#1136](https://github.com/ethyca/fides/pull/1136)

### Changed

- Update fideslang to v1.3.1 [#1136](https://github.com/ethyca/fides/pull/1136)

## [1.9.0](https://github.com/ethyca/fides/compare/1.8.6...1.9.0) - 2022-09-29

### Added

- Dataset generation enhancements using Fides Classify for Plus users:
  - Added toggle for enabling classify during generation. [#1057](https://github.com/ethyca/fides/pull/1057)
  - Initial implementation of API request to kick off classify, with confirmation modal. [#1069](https://github.com/ethyca/fides/pull/1069)
  - Initial Classification & Review status for generated datasets. [#1074](https://github.com/ethyca/fides/pull/1074)
  - Component for choosing data categories based on classification results. [#1110](https://github.com/ethyca/fides/pull/1110)
  - The dataset fields table shows data categories from the classifier (if available). [#1088](https://github.com/ethyca/fides/pull/1088)
  - The "Approve" button can be used to update the dataset with the classifier's suggestions. [#1129](https://github.com/ethyca/fides/pull/1129)
- System management UI:
  - New page to add a system via yaml [#1062](https://github.com/ethyca/fides/pull/1062)
  - Skeleton of page to add a system manually [#1068](https://github.com/ethyca/fides/pull/1068)
  - Refactor config wizard system forms to be reused for system management [#1072](https://github.com/ethyca/fides/pull/1072)
  - Add additional optional fields to system management forms [#1082](https://github.com/ethyca/fides/pull/1082)
  - Delete a system through the UI [#1085](https://github.com/ethyca/fides/pull/1085)
  - Edit a system through the UI [#1096](https://github.com/ethyca/fides/pull/1096)
- Cypress component testing [#1106](https://github.com/ethyca/fides/pull/1106)

### Changed

- Changed behavior of `load_default_taxonomy` to append instead of upsert [#1040](https://github.com/ethyca/fides/pull/1040)
- Changed behavior of adding privacy declarations to decouple the actions of the "add" and "next" buttons [#1086](https://github.com/ethyca/fides/pull/1086)
- Moved system related UI components from the `config-wizard` directory to the `system` directory [#1097](https://github.com/ethyca/fides/pull/1097)
- Updated "type" on SaaS config to be a simple string type, not an enum [#1197](https://github.com/ethyca/fides/pull/1197)

### Developer Experience

- Optional dependencies may have their version defined only once, in `optional-requirements.txt` [#1171](https://github.com/ethyca/fides/pull/1171)

### Docs

- Updated the footer links [#1130](https://github.com/ethyca/fides/pull/1130)

### Fixed

- Fixed the "help" link in the UI header [#1078](https://github.com/ethyca/fides/pull/1078)
- Fixed a bug in Data Category Dropdowns where checking i.e. `user.biometric` would also check `user.biometric_health` [#1126](https://github.com/ethyca/fides/pull/1126)

### Security

- Upgraded pymysql to version `1.0.2` [#1094](https://github.com/ethyca/fides/pull/1094)

## [1.8.6](https://github.com/ethyca/fides/compare/1.8.5...1.8.6) - 2022-09-28

### Added

- Added classification tables for Plus users [#1060](https://github.com/ethyca/fides/pull/1060)

### Fixed

- Fixed a bug where rows were being excluded from a data map [#1124](https://github.com/ethyca/fides/pull/1124)

## [1.8.5](https://github.com/ethyca/fides/compare/1.8.4...1.8.5) - 2022-09-21

### Changed

- Update fideslang to v1.3.0 [#1103](https://github.com/ethyca/fides/pull/1103)

## [1.8.4](https://github.com/ethyca/fides/compare/1.8.3...1.8.4) - 2022-09-09

### Added

- Initial system management page [#1054](https://github.com/ethyca/fides/pull/1054)

### Changed

- Deleting a taxonomy field with children will now cascade delete all of its children as well. [#1042](https://github.com/ethyca/fides/pull/1042)

### Fixed

- Fixed navigating directly to frontend routes loading index page instead of the correct static page for the route.
- Fix truncated evaluation error messages [#1053](https://github.com/ethyca/fides/pull/1053)

## [1.8.3](https://github.com/ethyca/fides/compare/1.8.2...1.8.3) - 2022-09-06

### Added

- Added more taxonomy fields that can be edited via the UI [#1000](https://github.com/ethyca/fides/pull/1000) [#1028](https://github.com/ethyca/fides/pull/1028)
- Added the ability to add taxonomy fields via the UI [#1019](https://github.com/ethyca/fides/pull/1019)
- Added the ability to delete taxonomy fields via the UI [#1006](https://github.com/ethyca/fides/pull/1006)
  - Only non-default taxonomy entities can be deleted [#1023](https://github.com/ethyca/fides/pull/1023)
- Prevent deleting taxonomy `is_default` fields and from adding `is_default=True` fields via the API [#990](https://github.com/ethyca/fides/pull/990).
- Added a "Custom" tag to distinguish user defined taxonomy fields from default taxonomy fields in the UI [#1027](https://github.com/ethyca/fides/pull/1027)
- Added initial support for enabling Fides Plus [#1037](https://github.com/ethyca/fides/pull/1037)
  - The `useFeatures` hook can be used to check if `plus` is enabled.
  - Navigating to/from the Data Map page is gated behind this feature.
  - Plus endpoints are served from the private Plus image.

### Fixed

- Fixed failing mypy tests [#1030](https://github.com/ethyca/fides/pull/1030)
- Fixed an issue where `fides push --diff` would return a false positive diff [#1026](https://github.com/ethyca/fides/pull/1026)
- Pinned pydantic version to < 1.10.0 to fix an error in finding referenced fides keys [#1045](https://github.com/ethyca/fides/pull/1045)

### Fixed

- Fixed failing mypy tests [#1030](https://github.com/ethyca/fides/pull/1030)
- Fixed an issue where `fides push --diff` would return a false positive diff [#1026](https://github.com/ethyca/fides/pull/1026)

### Docs

- Minor formatting updates to [Policy Webhooks](https://ethyca.github.io/fidesops/guides/policy_webhooks/) documentation [#1114](https://github.com/ethyca/fidesops/pull/1114)

### Removed

- Removed create superuser [#1116](https://github.com/ethyca/fidesops/pull/1116)

## [1.8.2](https://github.com/ethyca/fides/compare/1.8.1...1.8.2) - 2022-08-18

### Added

- Added the ability to edit taxonomy fields via the UI [#977](https://github.com/ethyca/fides/pull/977) [#1028](https://github.com/ethyca/fides/pull/1028)
- New column `is_default` added to DataCategory, DataUse, DataSubject, and DataQualifier tables [#976](https://github.com/ethyca/fides/pull/976)
- Added the ability to add taxonomy fields via the UI [#1019](https://github.com/ethyca/fides/pull/1019)
- Added the ability to delete taxonomy fields via the UI [#1006](https://github.com/ethyca/fides/pull/1006)
  - Only non-default taxonomy entities can be deleted [#1023](https://github.com/ethyca/fides/pull/1023)
- Prevent deleting taxonomy `is_default` fields and from adding `is_default=True` fields via the API [#990](https://github.com/ethyca/fides/pull/990).
- Added a "Custom" tag to distinguish user defined taxonomy fields from default taxonomy fields in the UI [#1027](https://github.com/ethyca/fides/pull/1027)

### Changed

- Upgraded base Docker version to Python 3.9 and updated all other references from 3.8 -> 3.9 [#974](https://github.com/ethyca/fides/pull/974)
- Prepend all database tables with `ctl_` [#979](https://github.com/ethyca/fides/pull/979)
- Moved the `admin-ui` code down one level into a `ctl` subdir [#970](https://github.com/ethyca/fides/pull/970)
- Extended the `/datamap` endpoint to include extra metadata [#992](https://github.com/ethyca/fides/pull/992)

## [1.8.1](https://github.com/ethyca/fides/compare/1.8.0...1.8.1) - 2022-08-08

### Deprecated

- The following environment variables have been deprecated, and replaced with the new environment variable names indicated below. To avoid breaking existing workflows, the deprecated variables are still respected in v1.8.1. They will be removed in a future release.
  - `FIDESCTL__API__DATABASE_HOST` --> `FIDESCTL__DATABASE__SERVER`
  - `FIDESCTL__API__DATABASE_NAME` --> `FIDESCTL__DATABASE__DB`
  - `FIDESCTL__API__DATABASE_PASSWORD` --> `FIDESCTL__DATABASE__PASSWORD`
  - `FIDESCTL__API__DATABASE_PORT` --> `FIDESCTL__DATABASE__PORT`
  - `FIDESCTL__API__DATABASE_TEST_DATABASE_NAME` --> `FIDESCTL__DATABASE__TEST_DB`
  - `FIDESCTL__API__DATABASE_USER` --> `FIDESCTL__DATABASE__USER`

### Developer Experience

- The included `docker-compose.yml` no longer references outdated ENV variables [#964](https://github.com/ethyca/fides/pull/964)

### Docs

- Minor release documentation now reflects the desired patch release process [#955](https://github.com/ethyca/fides/pull/955)
- Updated references to ENV variables [#964](https://github.com/ethyca/fides/pull/964)

### Fixed

- Deprecated config options will continue to be respected when set via environment variables [#965](https://github.com/ethyca/fides/pull/965)
- The git cache is rebuilt within the Docker container [#962](https://github.com/ethyca/fides/pull/962)
- The `wheel` pypi build no longer has a dirty version tag [#962](https://github.com/ethyca/fides/pull/962)
- Add setuptools to dev-requirements to fix versioneer error [#983](https://github.com/ethyca/fides/pull/983)

## [1.8.0](https://github.com/ethyca/fides/compare/1.7.1...1.8.0) - 2022-08-04

### Added

- Initial configuration wizard UI view
  - System scanning step: AWS credentials form and initial `generate` API usage.
  - System scanning results: AWS systems are stored and can be selected for review
- CustomInput type "password" with show/hide icon.
- Pull CLI command now checks for untracked/unstaged files in the manifests dir [#869](https://github.com/ethyca/fides/pull/869)
- Pull CLI command has a flag to pull missing files from the server [#895](https://github.com/ethyca/fides/pull/895)
- Add BigQuery support for the `generate` command and `/generate` endpoint [#814](https://github.com/ethyca/fides/pull/814) & [#917](https://github.com/ethyca/fides/pull/917)
- Added user auth tables [915](https://github.com/ethyca/fides/pull/915)
- Standardized API error parsing under `~/types/errors`
- Added taxonomy page to UI [#902](https://github.com/ethyca/fides/pull/902)
  - Added a nested accordion component for displaying taxonomy data [#910](https://github.com/ethyca/fides/pull/910)
- Add lru cache to get_config [927](https://github.com/ethyca/fides/pull/927)
- Add support for deprecated API config values [#959](https://github.com/ethyca/fides/pull/959)
- `fides` is now an alias for `fidesctl` as a CLI entrypoint [#926](https://github.com/ethyca/fides/pull/926)
- Add user auth routes [929](https://github.com/ethyca/fides/pull/929)
- Bump fideslib to 3.0.1 and remove patch code[931](https://github.com/ethyca/fides/pull/931)
- Update the `fidesctl` python package to automatically serve the UI [#941](https://github.com/ethyca/fides/pull/941)
- Add `push` cli command alias for `apply` and deprecate `apply` [943](https://github.com/ethyca/fides/pull/943)
- Add resource groups tagging api as a source of system generation [939](https://github.com/ethyca/fides/pull/939)
- Add GitHub Action to publish the `fidesctl` package to testpypi on pushes to main [#951](https://github.com/ethyca/fides/pull/951)
- Added configWizardFlag to ui to hide the config wizard when false [[#1453](https://github.com/ethyca/fides/issues/1453)

### Changed

- Updated the `datamap` endpoint to return human-readable column names as the first response item [#779](https://github.com/ethyca/fides/pull/779)
- Remove the `obscure` requirement from the `generate` endpoint [#819](https://github.com/ethyca/fides/pull/819)
- Moved all files from `fidesapi` to `fidesctl/api` [#885](https://github.com/ethyca/fides/pull/885)
- Moved `scan` and `generate` to the list of commands that can be run in local mode [#841](https://github.com/ethyca/fides/pull/841)
- Upgraded the base docker images from Debian Buster to Bullseye [#958](https://github.com/ethyca/fides/pull/958)
- Removed `ipython` as a dev-requirement [#958](https://github.com/ethyca/fides/pull/958)
- Webserver dependencies now come as a standard part of the package [#881](https://github.com/ethyca/fides/pull/881)
- Initial configuration wizard UI view
  - Refactored step & form results management to use Redux Toolkit slice.
- Change `id` field in tables from an integer to a string [915](https://github.com/ethyca/fides/pull/915)
- Update `fideslang` to `1.1.0`, simplifying the default taxonomy and adding `tags` for resources [#865](https://github.com/ethyca/fides/pull/865)
- Merge existing configurations with `fideslib` library [#913](https://github.com/ethyca/fides/pull/913)
- Moved frontend static files to `src/fidesctl/ui-build/static` [#934](https://github.com/ethyca/fides/pull/934)
- Replicated the error response handling from the `/validate` endpoint to the `/generate` endpoint [#911](https://github.com/ethyca/fides/pull/911)

### Developer Experience

- Remove `API_PREFIX` from fidesctl/core/utils.py and change references to `API_PREFIX` in fidesctl/api/reoutes/util.py [922](https://github.com/ethyca/fides/pull/922)

### Fixed

- Dataset field columns show all columns by default in the UI [#898](https://github.com/ethyca/fides/pull/898)
- Fixed the missing `.fides./` directory when locating the default config [#933](https://github.com/ethyca/fides/pull/933)

## [1.7.1](https://github.com/ethyca/fides/compare/1.7.0...1.7.1) - 2022-07-28

### Added

- Add datasets via YAML in the UI [#813](https://github.com/ethyca/fides/pull/813)
- Add datasets via database connection [#834](https://github.com/ethyca/fides/pull/834) [#889](https://github.com/ethyca/fides/pull/889)
- Add delete confirmation when deleting a field or collection from a dataset [#809](https://github.com/ethyca/fides/pull/809)
- Add ability to delete datasets from the UI [#827](https://github.com/ethyca/fides/pull/827)
- Add Cypress for testing [713](https://github.com/ethyca/fides/pull/833)
- Add datasets via database connection (UI only) [#834](https://github.com/ethyca/fides/pull/834)
- Add Okta support to the `/generate` endpoint [#842](https://github.com/ethyca/fides/pull/842)
- Add db support to `/generate` endpoint [849](https://github.com/ethyca/fides/pull/849)
- Added OpenAPI TypeScript client generation for the UI app. See the [README](/clients/admin-ui/src/types/api/README.md) for more details.

### Changed

- Remove the `obscure` requirement from the `generate` endpoint [#819](https://github.com/ethyca/fides/pull/819)

### Developer Experience

- When releases are published, dispatch a repository webhook event to ethyca/fidesctl-plus [#938](https://github.com/ethyca/fides/pull/938)

### Docs

- recommend/replace pip installs with pipx [#874](https://github.com/ethyca/fides/pull/874)

### Fixed

- CustomSelect input tooltips appear next to selector instead of wrapping to a new row.
- Datasets without the `third_country_transfer` will not cause the editing dataset form to not render.
- Fixed a build issue causing an `unknown` version of `fidesctl` to be installed in published Docker images [#836](https://github.com/ethyca/fides/pull/836)
- Fixed an M1-related SQLAlchemy bug [#816](https://github.com/ethyca/fides/pull/891)
- Endpoints now work with or without a trailing slash. [#886](https://github.com/ethyca/fides/pull/886)
- Dataset field columns show all columns by default in the UI [#898](https://github.com/ethyca/fides/pull/898)
- Fixed the `tag` specific GitHub Action workflows for Docker and publishing docs. [#901](https://github.com/ethyca/fides/pull/901)

## [1.7.0](https://github.com/ethyca/fides/compare/1.6.1...1.7.0) - 2022-06-23

### Added

- Added dependabot to keep dependencies updated
- A warning now issues for any orphan datasets as part of the `apply` command [543](https://github.com/ethyca/fides/pull/543)
- Initial scaffolding of management UI [#561](https://github.com/ethyca/fides/pull/624)
- A new `audit` command for `system` and `organization` resources, checking data map attribute compliance [#548](https://github.com/ethyca/fides/pull/548)
- Static UI assets are now built with the docker container [#663](https://github.com/ethyca/fides/issues/663)
- Host static files via fidesapi [#621](https://github.com/ethyca/fides/pull/621)
- A new `generate` endpoint to enable capturing systems from infrastructure from the UI [#642](https://github.com/ethyca/fides/pull/642)
- A new `datamap` endpoint to enable visualizing a data map from the UI [#721](https://github.com/ethyca/fides/pull/721)
- Management UI navigation bar [#679](https://github.com/ethyca/fides/issues/679)
- Management UI integration [#736](https://github.com/ethyca/fides/pull/736)
  - Datasets
  - Systems
  - Taxonomy (data categories)
- Initial dataset UI view [#768](https://github.com/ethyca/fides/pull/768)
  - Add interaction for viewing a dataset collection
  - Add column picker
  - Add a data category checklist tree
  - Edit/delete dataset fields
  - Edit/delete dataset collections
  - Edit datasets
  - Add a component for Identifiability tags
  - Add tooltips for help on forms
  - Add geographic location (third_country_transfers) country selection. Supported by new dependency `i18n-iso-countries`.
- Okta, aws and database credentials can now come from `fidesctl.toml` config [#694](https://github.com/ethyca/fides/pull/694)
- New `validate` endpoint to test aws and okta credentials [#722](https://github.com/ethyca/fides/pull/722)
- Initial configuration wizard UI view
  - Manual entry steps added (name and describe organization, pick entry route, and describe system manually including privacy declarations)
- A new image tagged `ethyca/fidesctl:dev` is published on each push to `main` [781](https://github.com/ethyca/fides/pull/781)
- A new cli command (`fidesctl sync`) [#765](https://github.com/ethyca/fides/pull/765)

### Changed

- Comparing server and CLI versions ignores `.dirty` only differences, and is quiet on success when running general CLI commands [621](https://github.com/ethyca/fides/pull/621)
- All endpoints now prefixed by `/api/v1` [#623](https://github.com/ethyca/fides/issues/623)
- Allow AWS credentials to be passed to `generate system` via the API [#645](https://github.com/ethyca/fides/pull/645)
- Update the export of a datamap to load resources from the server instead of a manifest directory [#662](https://github.com/ethyca/fides/pull/662)
- Refactor `export` to remove CLI specific uses from the core modules and load resources[#725](https://github.com/ethyca/fides/pull/725)
- Bump version of FastAPI in `setup.py` to 0.77.1 to match `optional-requirements.txt` [#734](https://github.com/ethyca/fides/pull/734)
- Docker images are now only built and pushed on tags to match when released to pypi [#740](https://github.com/ethyca/fides/pull/740)
- Okta resource scanning and generation now works with systems instead of datasets [#751](https://github.com/ethyca/fides/pull/751)

### Developer Experience

- Replaced `make` with `nox` [#547](https://github.com/ethyca/fides/pull/547)
- Removed usage of `fideslang` module in favor of new [external package](https://github.com/ethyca/fideslang) shared across projects [#619](https://github.com/ethyca/fides/issues/619)
- Added a UI service to the docker-compose deployment [#757](https://github.com/ethyca/fides/pull/757)
- `TestClient` defined in and shared across test modules via `conftest.py` [#759](https://github.com/ethyca/fides/pull/759)

### Docs

- Replaced all references to `make` with `nox` [#547](https://github.com/ethyca/fides/pull/547)
- Removed config/schemas page [#613](https://github.com/ethyca/fides/issues/613)
- Dataset UI and config wizard docs added ([https://github.com/ethyca/fides/pull/697](https://github.com/ethyca/fides/pull/697))
- The fides README now walks through generating a datamap [#746](https://github.com/ethyca/fides/pull/746)

### Fixed

- Updated `fideslog` to v1.1.5, resolving an issue where some exceptions thrown by the SDK were not handled as expected [#609](https://github.com/ethyca/fides/issues/609)
- Updated the webserver so that it won't fail if the database is inaccessible [#649](https://github.com/ethyca/fides/pull/649)
- Updated external tests to handle complex characters [#661](https://github.com/ethyca/fides/pull/661)
- Evaluations now properly merge the default taxonomy into the user-defined taxonomy [#684](https://github.com/ethyca/fides/pull/684)
- The CLI can now be run without installing the webserver components [#715](https://github.com/ethyca/fides/pull/715)

## [1.6.1](https://github.com/ethyca/fides/compare/1.6.0...1.6.1) - 2022-06-15

### Docs

- Updated `Release Steps`

### Fixed

- Resolved a failure with populating applicable data subject rights to a data map
- Handle invalid characters when generating a `fides_key` [#761](https://github.com/ethyca/fides/pull/761)

## [1.6.0](https://github.com/ethyca/fides/compare/1.5.3...1.6.0) - 2022-05-02

### Added

- ESLint configuration changes [#514](https://github.com/ethyca/fidesops/pull/514)
- User creation, update and permissions in the Admin UI [#511](https://github.com/ethyca/fidesops/pull/511)
- Yaml support for dataset upload [#284](https://github.com/ethyca/fidesops/pull/284)

### Breaking Changes

- Update masking API to take multiple input values [#443](https://github.com/ethyca/fidesops/pull/443)

### Docs

- DRP feature documentation [#520](https://github.com/ethyca/fidesops/pull/520)

## [1.4.2](https://github.com/ethyca/fidesops/compare/1.4.1...1.4.2) - 2022-05-12

### Added

- GET routes for users [#405](https://github.com/ethyca/fidesops/pull/405)
- Username based search on GET route [#444](https://github.com/ethyca/fidesops/pull/444)
- FIDESOPS\_\_DEV_MODE for Easier SaaS Request Debugging [#363](https://github.com/ethyca/fidesops/pull/363)
- Track user privileges across sessions [#425](https://github.com/ethyca/fidesops/pull/425)
- Add first_name and last_name fields. Also add them along with created_at to FidesUser response [#465](https://github.com/ethyca/fidesops/pull/465)
- Denial reasons for DSR and user `AuditLog` [#463](https://github.com/ethyca/fidesops/pull/463)
- DRP action to Policy [#453](https://github.com/ethyca/fidesops/pull/453)
- `CHANGELOG.md` file[#484](https://github.com/ethyca/fidesops/pull/484)
- DRP status endpoint [#485](https://github.com/ethyca/fidesops/pull/485)
- DRP exerise endpoint [#496](https://github.com/ethyca/fidesops/pull/496)
- Frontend for privacy request denial reaons [#480](https://github.com/ethyca/fidesops/pull/480)
- Publish Fidesops to Pypi [#491](https://github.com/ethyca/fidesops/pull/491)
- DRP data rights endpoint [#526](https://github.com/ethyca/fidesops/pull/526)

### Changed

- Converted HTTP Status Codes to Starlette constant values [#438](https://github.com/ethyca/fidesops/pull/438)
- SaasConnector.send behavior on ignore_errors now returns raw response [#462](https://github.com/ethyca/fidesops/pull/462)
- Seed user permissions in `create_superuser.py` script [#468](https://github.com/ethyca/fidesops/pull/468)
- User API Endpoints (update fields and reset user passwords) [#471](https://github.com/ethyca/fidesops/pull/471)
- Format tests with `black` [#466](https://github.com/ethyca/fidesops/pull/466)
- Extract privacy request endpoint logic into separate service for DRP [#470](https://github.com/ethyca/fidesops/pull/470)
- Fixing inconsistent SaaS connector integration tests [#473](https://github.com/ethyca/fidesops/pull/473)
- Add user data to login response [#501](https://github.com/ethyca/fidesops/pull/501)

### Breaking Changes

- Update masking API to take multiple input values [#443](https://github.com/ethyca/fidesops/pull/443)

### Docs

- Added issue template for documentation updates [#442](https://github.com/ethyca/fidesops/pull/442)
- Clarify masking updates [#464](https://github.com/ethyca/fidesops/pull/464)
- Added dark mode [#476](https://github.com/ethyca/fidesops/pull/476)

### Fixed

- Removed miradb test warning [#436](https://github.com/ethyca/fidesops/pull/436)
- Added missing import [#448](https://github.com/ethyca/fidesops/pull/448)
- Removed pypi badge pointing to wrong package [#452](https://github.com/ethyca/fidesops/pull/452)
- Audit imports and references [#479](https://github.com/ethyca/fidesops/pull/479)
- Switch to using update method on PUT permission endpoint [#500](https://github.com/ethyca/fidesops/pull/500)

### Developer Experience

- added isort as a CI check
- Include `tests/` in all static code checks (e.g. `mypy`, `pylint`)

### Changed

- Published Docker image does a clean install of Fidesctl
- `with_analytics` is now a decorator

### Fixed

- Third-Country formatting on Data Map
- Potential Duplication on Data Map
- Exceptions are no longer raised when sending `AnalyticsEvent`s on Windows
- Running `fidesctl init` now generates a `server_host` and `server_protocol`
  rather than `server_url`