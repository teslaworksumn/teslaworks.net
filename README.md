teslaworks.net
==============

New web app for the University of Minnesota Tesla Works student organization

This is my first foray into the big, bad world of designing a Rails application without some tutorial giving me each little snippet of code to type as I go along. I'm betting this is going to be one big mistake-fest, and that I'm going to learn a lot from it. Let's get cracking!

Goals for the Website
---------------------

* First and foremost, make it easy to learn about and join our current projects
  * What is the project?
  * What has been done so far?
  * What needs to be done?
  * How can I start?
* Collect news, including:
  * Significant project accomplishments
  * New project announcements
  * General group news
  * Meeting reminders/descriptions
* Make it easy to find out about TW past accomplishments

Design Philosophy
-----------------

* We want the site to be *an app*. We don't want it to be a static page— we want it to be interactive, ever-changing, and up-to-date
* We want the app to do *as few things as possible*, and *combine functionality* wherever possible
* In general, all related information needs to be displayed on *one long page*, __not__ multiple sub-pages

Integrations
------------

### Basecamp

* Open to-dos on a project show up on the project page
* One-click join Basecamp
* Sort projects on site home page by most recent Basecamp activity (daily updates?)

Design Implementation Notes
---------------------------

* Pagination should be scrolling-enabled, not click-enabled
* Prefer to have the smallest number of possible templates, with very unique UI elements for each
