Norikra-client-python
============================

client library of norikra-client.

Note: This does not include CLI, only library.

Install
--------

::

  % pip install -e "git+https://github.com/shirou/norikra-client-python.git"

Usage
----------

::

  from norikraclient.client import Client

  norikra = Client()
  norikra.send('your_target', [{'ham': 'spam'}])

License
-----------

MIT License
