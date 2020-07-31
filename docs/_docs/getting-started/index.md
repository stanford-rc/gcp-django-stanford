---
title: Getting Started
tags: 
 - jekyll
 - github
description: Getting started with the template
---

# Getting Started

The documentation here will get you started to use the gcp-django-template, developed
with Python and Django. This is intended for developers. If you want to see
the user documentation, see [the user guide]({{ site.baseurl }}/user-guide/).

## Setup

You will want to follow the instructions [here](https://cloud.google.com/appengine/docs/standard/python3/building-app/writing-web-service)
and:

 - create a Google Cloud Project, you can request one at Stanford [here](https://stanford.service-now.com/it_services?id=sc_cat_item&sys_id=fa9f80bddbf05b401df130cf9d96198b)
 - install the gcloud command line client and Python3+
 - authenticate on the command line with `gcloud auth application-default login`

For example, after I've created my project and I've installed gcloud, I might login and
then set the default project to be my new project:

```bash
$ gcloud auth application-default login
$ gcloud config set project <myproject>
```

Then to work locally (if you are developing) you'll want to clone the project:

```bash
git clone https://github.com/vsoch/gcp-django-stanford
cd gcp-django-stanford
```

On the [Google Project Console](https://console.developers.google.com/apis) you might want to enable
APIs for the following:

 - Identity and Access Management (IAM) API
 - Google Storage


### Storage

Since app engine doesn't allow writing to the filesystem, you would need to use Google Cloud Storage
for file uploads, and use the [django-storages](https://django-storages.readthedocs.io/en/latest/backends/gcloud.html)
library to do this (not yet developed, but please [ask for this feature]({{ site.repo }}/issues) if you need it).

### Billing

Under billing, it's good practice to also set up billing alerts - unintended charges to a project that you don't know about can have dire consequences. A small server of this size shouldn't cost more than $55 a  month (this would be a LOT) so I generally would start with a lower monthly limit (possibly $55) with alerts at 25, 50, 75, and 100 percents, and adjust as needed.


### Configuration

The application has a set of configuration variables that are discovered in the environment
via an .env file that you can source before running the application, and these
environment variables are also given to the app engine app.yaml file so they are discovered
on App Engine. When you first start out, you can copy the dummy template provided in
the repository:

```bash
cp .dummy-env .env
```

and also copy the app-example.yaml to an app.yaml file (that will contain secrets and not be
included in the repository):

```bash
cp app-example.yaml app.yaml
```

For local development, you will want to populate the following configuration variables the the .env file:


#### Secret Key

A secret key is used to secure your server. You can use the [secret key generator](https://djecrety.ir/) to make a new secret key, and also export it as the `DJANGO_SECRET_KEY` in your `.env` file:

```bash
export DJANGO_SECRET_KEY=123455
```

#### Terms of Service

By default, when logging in for the first time the user account is required to read your
terms of service and agree. The agreement timestamp is saved with the user account.
In order for this to work, it's suggested to create a google document, and then
pulish it to a URL, and then export it in your .env file:

```bash
export TERMS_OF_SERVICE_URL=https://docs.google.com/document/d/e/xxxx/pub?embedded=true
```

#### Google Analytics

If you want to use [Google Analytics](https://analytics.google.com/analytics/web/) with your application, generate a key and add
it to your application, again in the `.env` file.

```bash
export GOOGLE_ANALYTICS_ID=1111111111111111
```

#### Social Networks

If you want a twitter card / alias embedded in site metadata, export the `TWITTER_USERNAME` in your .env file.

```bash
export TWITTER_USERNAME=vsoch
```

You can also easily link to an instagram or facebook.

```
export FACEBOOK_USERNAME=dinosaur
export INSTAGRAM_USERNAME=dinosaur
```

These last two are undefined by default and won't show on the site.

#### Authentication 

The interface currently assumes that the "backend" (ability to log in) is done via
invite only, and so the typical registration form is not provided. If you would like help
to add a standard registration form or other forms of authentication (social auth, SAML, etc.)
please [ask for this feature]({{ site.repo }}/issues).
This means that an administrator is responsible for adding new users. 


#### Help Contact Email

To provide users with a contact form, although the site uses SendGrid for more
bulk emails, we use [formspree](https://formspree.io/) to drive the contact form, which better
handles spam. You should export your `HELP_CONTACT_EMAIL` in the .env file as follows:

```
export HELP_CONTACT_EMAIL=myemail@domain.com
```

### SendGrid

We use SendGrid to invite users to the site. Note that the emails can sometimes
end up in spam, so you should be prepared to notify invitees of this.

#### SendGrid Sender Email

You'll need a `SENDGRID_SENDER_EMAIL` exported in your .env file in order to use
SendGrid:

```
export SENDGRID_SENDER_EMAIL=myemail@domain.com
```

If this is the same as your `HELP_CONTACT_EMAIL` you can leave it blank, and the help
contact email will be used. **Important** before using the API this email needs to be added as a known [Sender](https://app.sendgrid.com/settings/sender_auth/senders). If it is not, you will get a permission denied error. You
also likely want to go to Settings -> Tracking and disable link tracking in email.

#### SendGrid Account

To send emails from the server, we use SendGrid. This means
that you need to [sign up](https://app.sendgrid.com/) for an account (the basic account with 100 emails
per day is free) and then add the `SENDGRID_API_KEY` to your .env file:

```python
export SENDGRID_API_KEY=xxxxxxxxxxxxxxx
```

Then to create your key:

 1. Go to [SendGrid](https://app.sendgrid.com/) and click on Settings -> Api keys in the left bar
 2. Click the blue button to "Create API key"
 3. Give your key a meaningful name (e.g., freegenes_dev_test)
 4. Choose "Restricted Access" and give "Full Access" to mail send by clicking the bar on the far right circle.
 5. Copy it to a safe place, likely your settings/config.py (it is only shown once!)

If the value is found to be None, emails will not be sent.


### Rate Limits

It's hard to believe that anyone would want to maliciously issue requests to your server,
but it's unfortunately a way of life. For this reason, all views have a rate limit, along
with blocking ip addresses that exceed it (for the duration of the limit, one day). You
can customize this:

```python
VIEW_RATE_LIMIT="50/1d"  # The rate limit for each view, django-ratelimit, "50 per day per ipaddress)
VIEW_RATE_LIMIT_BLOCK=True # Given that someone goes over, are they blocked for the period?
```
And see the [django-ratelimit](https://django-ratelimit.readthedocs.io/en/v1.0.0/usage.html) documentation
for other options. 

## Development

To develop locally, you'll want to create a local environment and then install
dependencies to it.

```bash
python -m venv env
source env/bin/activate
pip install  -r requirements.txt
```

And always source this environment before you start working.
Then you will want to source your environment file:

```bash
source .env
```

To make migrations we usually might do this:

```bash
python manage.py makemigrations
python manage.py makemigrations main
python manage.py migrate
```

But to make it easier, there is an included Makefile that can be used to make
migrations, and then migrate.

```bash
make migrations
make migrate
```

Then we would typically use the `manage.py` to run the server.

```bash
python manage.py runserver
```

But there is also a make command that is easier to type:

```bash
make run
```

And then you can open up your browser to [http://localhost:8000](http://localhost:8000).


### Database

For our database, we use [Stanford managed SQL](https://uit.stanford.edu/service/sql).
We won't need this for local development, for which we will use sqlite (a local file database).
If you ever need to delete and refresh this local testing database, you can do:

```bash
rm db.sqlite3
```

For deployment, you'll need to first create your database in cloud managed sql,
and export these environment variables in your local .env file:

```
export MYSQL_HOST=<the.hostname>
export MYSQL_USER=<dbusername>
export MYSQL_PASSWORD=<dbpassword>
export MYSQL_DATABASE=<databasename>
```

And then at the onset of development, you'll need to both make and run migrations.

```bash
make migrate
make migrations
```


### Models

The core of any Django application is the definition of [models](https://docs.djangoproject.com/en/3.0/topics/db/models/).
A model maps directly to a database table, so when you originally design your application, you will
want to spend some time on this design. The current application creates dummy models for users, an organization,
and then associated projects. You can also imagine having models for a biological entity, or some kind
of machine learning model.  Please reach out to [RSE Services]({{ site.repo }}/issues) if you want any help
designing your models.


### Sentry for Monitoring

We can create a few account on [sentry.io](https://sentry.io/) to set up logging
for our application, and be alerted if there are any errors. The steps there will
walk you through setup, although you primarily just need to export the id number
as `SENTRY_ID` in your local .env and app.yaml.

```bash
export SENTRY_ID=https://xxxxxxxxxxxxxxxxxxxxxxxxxxx.ingest.sentry.io/111111
```

Don't add this until you are ready to start getting error reports (e.g., when testing locally
and Debug modeis true you don't need it).



### Testing

You can write tests for your models, and an example is provided in the repository "tests" folder.
You can run tests locally after sourcing your environent, and using the `manage.py test` command.

```bash
source env/bin/activate
python manage.py test tests.test_project
```

You can see the [Django docs for testing](https://docs.djangoproject.com/en/3.0/topics/testing/overview/) for more details.

### Deployment

#### 1. Request Stanford AFS

If you don't have a group on Stanford AFS, then you should [first request one](https://uit.stanford.edu/service/afs). This typically
maps to a folder in the Stanford AFS web space, and we need this space to create a database there.

#### 2. Request Stanford Managed SQL

Once you have the folder, you can self-request [Stanford managed SQL](https://uit.stanford.edu/service/sql).
and the screen will take you immediately to a page with credentials to write into your .env file (for local setup)
and your app.yaml (for deployment, discussed next).

#### 3. Populate app.yaml

The app.yaml file that you created from the app-example.yaml (which you absolutely should not
put environment variables in) should be populated with your environment variables from the .env
file, along with your database credentials. As stated above, since we want to initialize the database from
our local machine, we should also write them to the .env file.

#### 4. Remove Migrations

Since we are starting with a fresh database, we can safely remove the many migrations that we made
for testing.

```bash
rm -rf gcpdjango/apps/users/migrations/
rm -rf gcpdjango/apps/main/migrations
```

#### 5. Setup Database Locally

If you haven't already, source your environment with the newly added database:

```bash
source env/bin/activate
source .env
```

And then collect static, make migrations, and migrate. This should again create new
database tables.

```bash
make collect
make migrations
make migrate
```

You can then run the server locally (using the now relational database instead of sqlite)
and see the interface. You can add yourself (and another if needed) as a superuser:

```bash
python manage.py createsuperuser
```

And remember if you want someone to be added to the admin console, they need to be
added as follows:

```bash
python manage.py add_superuser <username>
```

#### 6. Add your Group

Since we added ourselves as users to the interface, we will want to
edit our user to be associated with a center in the admin console. You can
create groups at `http://127.0.0.1:8000/admin/users/group/` and then edit users
(adding them to a group) at `<hostname>/admin/users/user/` (`http://127.0.0.1:8000/admin/users/user/`).
You won't need to do this for all subsequent users that are invited via email,
as they will select their group upon registration. This flow can of course be changed
to allow for user registration, or login with social or other authentication.

#### 7. Test the local interface

And then log in to the interface! It's good to look/test things now locally
before deployment to make sure it works as expected.

```bash
make run
```

#### 8. Google Cloud Permissions

Make sure that app engine is enabled, and that your user account (the email
associated with your project) has create permissions for it. If you don't,
you will get a permission denied:

```bash
ERROR: (gcloud.app.create) PERMISSION_DENIED: The caller does not have permission
```

then you should go the IAM and Admin tab and ensure that the account associated with
your user email (on your local machine) has proper permissions. If when you are doing 
the deployment you get a similar error:

```bash
ERROR: (gcloud.app.deploy) Error Response: [9] Cloud build 99bd2f7d-b098-41a8-9841-xxxxxxxx status: FAILURE
Build error details: Access to bucket staging.<project>.appspot.com denied. You must grant Storage Object Viewer permission to xxxxxxxx@cloudbuild.gserviceaccount.com.
```

Then simply follow the instruction! Google permissions are kind of hairy, and
I've seen different behavior over time. It's best to grant the minimal permissions
you think are needed, and then adjust if necessary based on these messages.

#### 9. Deploy

When you are ready, let's deploy to app engine! Remember that your app.yaml
should be entirely populated. This is where your `.gcloudignore` is important -
anything that you don't want uploaded to your project should be written there.
If you have been working on other projects, make sure that the project
associated with your account is active:

```bash
$ gcloud config set project <myproject>
```

```bash
$ gcloud app create --project=<myproject>
```

When you are ready, deploy your app!

```bash
$ gcloud app deploy
Initializing App Engine resources...done.                                                                                                
Services to deploy:

descriptor:      [/home/vanessa/Desktop/Code/gcp-django-stanford/app.yaml]
source:          [/home/vanessa/Desktop/Code/gcp-django-stanford]
target project:  [project]
target service:  [default]
target version:  [xxxxxxxxx]
target url:      [https://<project>.<region_id>.r.appspot.com]

Do you want to continue (Y/n)?  y

Beginning deployment of service [default]...
╔════════════════════════════════════════════════════════════╗
╠═ Uploading 313 files to Google Cloud Storage                ═╣
╚════════════════════════════════════════════════════════════╝
File upload done.
Updating service [default]...done.                                             
Setting traffic split for service [default]...done.                            
Deployed service [default] to [https://som-mhttcnco.uc.r.appspot.com]

You can stream logs from the command line by running:
  $ gcloud app logs tail -s default

To view your application in the web browser run:
  $ gcloud app browse
```

In the above we see:

 - a confirmation of app metadata
 - files uploaded to Google Storage
 - the final deployed URL.
 - commands to show logs, or open to the url (browse).

Note that the .gcloudignore file is important to not upload your docs, Python environment,
or other metadata or secrets. Speaking of environment variables, if you need additional ones 
 you can add them to your [app.yml file](https://cloud.google.com/appengine/docs/standard/python/config/appref). Indeed, if you needed to write all of these functions (e.g., build a container, have static files uploaded to storage, etc.) it would have been very cumbersome. But this deployment is in fact incredibly easy! App Engine is great because you pay for what you use, and
the base containers are maintained for you. And a few final tips:

 - if you need to re-do the storage upload, you can delete the buckets entirely (both for staging and production) and they will be re-generated.

## Cleaning Up

You should navigate to App Engine --> Settings and then click on "Disable Application" to permanently disable it.
Cleaning up also then means:

 - deleting the production and staging storage buckets for your app
 - deleting the storage artifacts bucket (e.g., logs) if they are not needed.

Remember, your app.yml that has environment variables  **must not be added to a public
GitHub repository, or even a private one for that matter!**

The complete details for this deployment are [here](https://cloud.google.com/python/django/appengine#deploying_the_app_to_the_standard_environment_).
