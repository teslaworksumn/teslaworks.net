teslaworks.net
==============

Hey! This is the repository for Tesla Works' [teslaworks.net](http://teslaworks.net) homepage. Key functions of this page include:

1. Providing persuasion and a clear path for people to join our projects
2. Helping people understand what our group does
3. Providing functionality such as purchasing and starting new projects for existing members

If you'd like to make a suggestion for an improvement, just [search for existing reported issues](https://github.com/teslaworksumn/teslaworks.net/search?q=search+here&type=Issues) and add a new one if none already exists!

Getting Started
---------------

Down and dirty, this will get you up and running for development.

Dependencies:
- Python 2.7+
- `pip`
- Flask
- a Sass (really, SCSS) compiler

First, you must create a valid configuration file for teslaworks.net. Follow the guidance in the configuration section below.

Next, run the following commands:

```
$ git clone https://github.com/teslaworksumn/teslaworks.net.git
$ cd teslaworks.net
$ pip install -r requirements.txt
$ mkdir static/css
$ sass sass/teslaworks.scss static/css/teslaworks.css
$ python server_dev.py
```

You should be able to visit `http://localhost:5000/` and see the website up and running! If you're using our database, you might have project data already. Otherwise, you'll have to add it yourself. See the database section for more information.

Long-Term Maintainers
---------------------

This project is built using a myriad of carefully chosen technologies, most of which are seriously fun to use! Maintainers should have a good working knowledge of the following technologies:

- Flask + Jinja2
- PostgreSQL
- Bootstrap3
- Sass
- JQuery
- Tumblr
- Mailgun
- Sentry
- Mixpanel
- Basecamp API
- Docker
- uWSGI
- Nginx
- `supervise`

Maintainers of this project should have an earnest desire to work diligently on good content strategy for the group, understand and improve website performance, and understand and improve the site's design.

Technologies
------------

### Site Content

<!-- TODO: Discuss Tesla Works voice and messaging -->

To update project data, information about project leaders, and special redirects, you'll currently need to directly update the database. Layout of the database can be gleaned from `external/postgres/create-tables.sql`.

Photo dimensions were chosen to look best on Retina displays. Be aware of maximum image sizings for different screen sizes! Our projects grid on the home page is widest on mobile devices, since the grid becomes a vertical list.

| Photo Dimensions          | Width       | Height      |
|---------------------------|-------------|-------------|
| Home page jumbotron       | ???         | ???         |
| Front page projects       | 1500px      | 1000px      |
| Project details           | 1500px      | 1000px      |
| Project leaders           | 500px       | 500px       |

### Possible Basecamp Integrations

*Not here yet, but on their way*

1. Link to project on Basecamp from project page
2. Add people to Basecamp from the "Join" button
3. Sort projects on Home page by Basecamp activity level
4. Show upcoming dates
5. Automatically populate project title and short description

### Tumblr

We use Tumblr to host our "News" page. The theme is in [[external/tumblr/theme.html]], and must be manually deployed.

### Tests

We have virtually no tests written, and don't really use them anyway. For a list of tests that need to be written, visit our [tests wiki](https://github.com/teslaworksumn/teslaworks.net/wiki/Tests).

Configuration
-------------

A sample configuration file ([[sample_config.py]]) is provided and must be renamed to `config.py` and populated with real data before being used. You may have to create a few accounts if you're not "one of us" and we can't hand out the passwords.

No configuration setting is optional.

`SECRET_KEY`: In order to prevent malicious parties from playing with our app's cookies and flash messages, we need to set a secret key for our app to use. It should be fairly long and sufficiently random, probably generated. On Macs, the `uuidgen` function works nicely.
`MIXPANEL_TOKEN`: Obtained from Mixpanel for a specific project. Use a different token for production and development to keep production data fairly accurate.
`MIXPANEL_SUPPRESS_SEND`: Another way to protect production data. When set to `True`, Mixpanel events won't be sent.

`CONTACT_EMAIL`: The recipient of emails from the Mailgun mailer when the app is in production.
`DEBUG_EMAIL`: The recipient of emails from the Mailgun mailer when the app is in development.

`DEBUG`: __Never__ set this to `True` in production. When `True`, helpful developer diagnostic logging and debugger screens are activated and the `DEBUG_EMAIL` is used as the recipient when sending emails from the mailer. These screens can be used to hijack the app in production, so __don't do it__.
`TESTING`: Set to `True` when running tests on our app.

`MAIL_SETTINGS`: Can be filled in using information from your Mailgun account.
`SENTRY_DSN`: An identifier you can find on your Sentry account. Use a separate project for production and development.
`DB_SETTINGS`: You'll need a properly configured Postgres database to hold project information and more. Use a separate database for production and development.

License
-------

All source code is open source and released under the MIT License. Content and images, however, belong to Tesla Works and shouldn't be duplicated anywhere. Feel free to use our theming and layouts, though.

See [[LICENSE]] for more information.

Deploying
---------

Never put any sensitive data in this repository! It is public.

We instead have a separate private repository with Dockerfile, private (secret) configuration information, nginx configuration, run scripts, and more. Use that to deploy.
