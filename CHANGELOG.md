Freshermeat Changelog
=====================

## 0.6 (2018-10-02)

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
  [#10](https://gitlab.com/cedric/Freshermeat/issues/10);
- the statistics page has been improved with two new charts: a pie chart for
  the activity of the projects and a pie for the number of projects submitted
  per contributor. The tag cloud has also been improved;
- added social share buttons for projects
  [#8](https://gitlab.com/cedric/Freshermeat/issues/8);
- the dashboard for administrators has been improved;
- the layout of the services page has been improved;
- fixed a bug: Hardcoded url in about box (to register your project)
  [#9](https://gitlab.com/cedric/Freshermeat/issues/9);
- various UI improvements.

## 0.4.0 (2018-06-05)

- It is now possible to import project from GitLab or GitHub just by giving
  an URL [#7](https://gitlab.com/cedric/Freshermeat/issues/7);
- It is also possible to add new projects thanks to a bookmarklet;
- Pages have now meaningful titles
  [#5](https://gitlab.com/cedric/Freshermeat/issues/5);
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
