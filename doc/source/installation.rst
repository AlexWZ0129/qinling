Qinling Installation Guide
==========================

Prerequisites
~~~~~~~~~~~~~

It is necessary to install some specific system libs for installing Qinling.
They can be installed on most popular operating system using their package
manager (for Ubuntu - *apt*, for Fedora - *dnf*, CentOS - *yum*, for Mac OS -
*brew* or *macports*).
The list of needed packages is shown below:

1. **python-dev**
2. **python-setuptools**
3. **python-pip**
4. **libffi-dev**
5. **libxslt1-dev (or libxslt-dev)**
6. **libxml2-dev**
7. **libyaml-dev**
8. **libssl-dev**

In case of Ubuntu, just run::

    $ apt-get install -y python-dev python-setuptools python-pip libffi-dev libxslt1-dev \
      libxml2-dev libyaml-dev libssl-dev

**NOTE:** **Qinling can be used without authentication at all or it can work
with OpenStack.** In case of OpenStack, it works **only on Keystone v3**, make
sure **Keystone v3** is installed.

Installation
~~~~~~~~~~~~

First of all, clone the repo and go to the repo directory::

    $ git clone https://github.com/openstack/qinling.git
    $ cd qinling

Generate config::

    $ tox -egenconfig

Configure Qinling as needed. The configuration file is located in
``etc/qinling.conf.sample``. You will need to modify the configuration options
and then copy it into ``/etc/qinling/qinling.conf``.
For details see :doc:`Qinling Configuration Guide </guides/configuration_guide>`

**Virtualenv installation**::

    $ tox

This will install necessary virtual environments and run all the project tests.
Installing virtual environments may take significant time (~10-15 mins).

**Local installation**::

    $ pip install -e .

or::

    $ pip install -r requirements.txt
    $ python setup.py install

**NOTE**: Differences *pip install -e* and *setup.py install*. **pip install -e**
works very similarly to **setup.py install** or the EasyInstall tool, except
that it doesn’t actually install anything. Instead, it creates a special
.egg-link file in the deployment directory, that links to your project’s
source code.

Before the first run
~~~~~~~~~~~~~~~~~~~~

After installation you will see **qinling-server** and **qinling-db-manage** commands
in your environment, either in system or virtual environment.

**NOTE**: In case of using **virtualenv**, all Qinling related commands available via
**tox -evenv --**. For example, *qinling-server* is available via
*tox -evenv -- qinling-server*.

**qinling-db-manage** command can be used for migrations.

For updating the database to the latest revision type::

    $ qinling-db-manage --config-file <path-to-qinling.conf> upgrade head

Before starting Qinling server, run *qinling-db-manage populate* command.
It prepares the DB, creates in it with all standard actions and standard
workflows which Qinling provides for all Qinling users.::

    $ qinling-db-manage --config-file <path-to-qinling.conf> populate

For more detailed information about *qinling-db-manage* script please see :doc:`Qinling Upgrade Guide </guides/upgrade_guide>`.

**NOTE**: For users who want a dry run with **SQLite** database backend(not
used in production), *qinling-db-manage* is not recommended for database
initialization because of `SQLite limitations <http://www.sqlite.org/omitted.html>`_.
Please use sync_db script described below instead for database initialization.

**If you use virtualenv**::

    $ tools/sync_db.sh --config-file <path-to-qinling.conf>

**Or run sync_db directly**::

    $ python tools/sync_db.py --config-file <path-to-qinling.conf>

Running Qinling API server
~~~~~~~~~~~~~~~~~~~~~~~~~~

To run Qinling API server perform the following command in a shell::

    $ qinling-server --server api --config-file <path-to-qinling.conf>

Running Qinling Engines
~~~~~~~~~~~~~~~~~~~~~~~

To run Qinling Engine perform the following command in a shell::

    $ qinling-server --server engine --config-file <path-to-qinling.conf>

Running Qinling Task Executors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To run Qinling Task Executor instance perform the following command in a shell::

    $ qinling-server --server executor --config-file <path-to-qinling.conf>

Note that at least one Engine instance and one Executor instance should be
running so that workflow tasks are processed by Qinling.

Running Multiple Qinling Servers Under the Same Process
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To run more than one server (API, Engine, or Task Executor) on the same process,
perform the following command in a shell::

    $ qinling-server --server api,engine --config-file <path-to-qinling.conf>

The --server command line option can be a comma delimited list. The valid
options are "all" (by default if not specified) or any combination of "api",
"engine", and "executor". It's important to note that the "fake" transport for
the rpc_backend defined in the config file should only be used if "all" the
Qinling servers are launched on the same process. Otherwise, messages do not
get delivered if the Qinling servers are launched on different processes
because the "fake" transport is using an in process queue.

Qinling Client Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Please refer to :doc:`Qinling Client / CLI Guide </guides/mistralclient_guide>`
