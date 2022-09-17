.. Shardz - Master documentation master file, created by
   sphinx-quickstart on Sat Sep 17 21:56:31 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Home page
=========

.. IMPORTANT::

   Please note that this documentation is a technical documentation meant for developers that want to contribute to the project.
   If you are an user, please refer to the `main documentation <https://github.com/Exanis/shardz/>`_.

Shardz Master is the master server component for Shardz. It is responsible for logging in users (delegating it to the authentication server)
and sending the servers list to the user.

Most of Shardz Master's functionnalities are merely proxies - it is sending data to the authentication and game server. There is no direct
connection from this server to any database, as it is intended to be agnostic of any kind of storage.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   ./routers.rst
   ./tools.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
