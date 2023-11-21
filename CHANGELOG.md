Freshermeat Changelog
=====================

## 0.9.0 (not yet released)

### Improvements

- Improvements to the releases worker;
- updated Wed editor for the description of the projects;
- open external links with noopenner noreferrer attributes;


### Fixes

- fixes in the templates for the list of projects, project details;
- fixed an issue in the list of news dedicated to the projects;
- fixed the serialization of the data in the API (for the news);

### Changes

- updated all JavaScript and Python dependencies;



## 0.8.1 (2022-05-06)

### Changes

- migrated all commands to the internal Flask Command Line Interface;
- fixed issues in async workers due to new syntax.


## 0.8.0 (2022-04-25)

### New

- a new API based on Flask-RESTX is now available and replaces the previous API.
  It is documented with Swagger.

### improvements

- the JavaScript code of the templates has been improved;
- all back-end and front-end dependencies are now up-to-date.


## 0.7.0 (2019-09-07)

### New

- added basic worker to retrieve project's news. News are listed in the
  project details page.
- added an RSS feed for the news of a project;
- added an RSS feed for the recent news of all projects;
- added a spinner during the loading of the project's information;
- added a view in order to let an administrator accept a submission (project
  to be added in the database);
- introduction of statistics per organizations (organization/<org-name>);
- added a route which returns an atom feed of CVEs.
- added global recent CVEs ATOM feed in the layout template.

### Changes

- Font-Awesome has been replaced by Fork-Awesome;
- the endpoint project of the API now returns less data (performance
  improvement).
- various improvements in the back-end and bug fixes.


## 0.6.0 (2018-10-02)

- added the possibility for any user to submit a project to the directory;
- added the possibility to define dependents and dependencies for projects;
- added the possibility to import projects from any GitLab instances (even the
  tags);
- added the possibility to delete a release;
- improved the statistics page. Mainly the graph of projects activity which is
  now clickable;
- improved the template for the project description page;
- improved the releases fetcher;
- improved the dashboard for administrators.

## 0.5.0 (2018-06-27)

- implemented similar projects
  [#10](https://git.sr.ht/~cedric/freshermeat/issues/10);
- the statistics page has been improved with two new charts: a pie chart for
  the activity of the projects and a pie for the number of projects submitted
  per contributor. The tag cloud has also been improved;
- added social share buttons for projects
  [#8](https://git.sr.ht/~cedric/freshermeat/issues/8);
- the dashboard for administrators has been improved;
- the layout of the services page has been improved;
- fixed a bug: Hardcoded url in about box (to register your project)
  [#9](https://git.sr.ht/~cedric/freshermeat/issues/9);
- various UI improvements.

## 0.4.0 (2018-06-05)

- It is now possible to import project from GitLab or GitHub just by giving
  an URL [#7](https://git.sr.ht/~cedric/freshermeat/issues/7);
- It is also possible to add new projects thanks to a bookmarklet;
- Pages have now meaningful titles
  [#5](https://git.sr.ht/~cedric/freshermeat/issues/5);
- A new profile page for non-admin users has been added;
- The name of the instance is configurable;
- Improved the layout of the page to create/edit projects;
- Improved the layout of the navbar and dropdown menus.

## 0.3.1 (2018-03-13)

- Improved the layout for medium and small screens;
- A new release now automatically update the attribute ``last_updated`` of a
  project.

## 0.3.0 (2018-03-03)

- New dashboard for administrators;
- Added a chart in order to display the distribution of organizations types;
- Only administrators are allowed to associate a project to an organization;
- It is now possible to filter organizations by type (Governmental, Private,
  Non-Profit, Education, etc.).

## 0.2.0 (2018-02-24)

- Added full-text search on description of projects;
- Added search on organization names from the organizations page;
- Added search on licenses, tags and languages (accessible via the charts of the
  statistics page);
- Improved layout of organization pages;
- It is now possible to add a logo for an organization.

## 0.1.0 (2018-01-15)

- major improvements of the database model;
- it is now possible to associate tags, licenses and languages to projects;
- a new page 'statistics' displays some charts about the most used licenses,
  languages and tags;
- it is possible to define several services based on a project;
- added pagination menu for the list of projects;
- improvements for the CVE and releases workers;
- various UI improvements and bug fixes.

## 0.0.1 (2018-01-03)

- first beta release of Freshermeat.
- basic functions are working: GitHub releases tracking, CVE tracking,
  subscribe to releases of projects via an ATOM feed, management of
  projects, search by tags, organizations and licenses.
