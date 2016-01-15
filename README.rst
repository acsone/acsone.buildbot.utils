=====================
acsone.buildbot.utils
=====================

.. image:: https://img.shields.io/badge/licence-GPL--2-blue.svg
   :target: http://www.gnu.org/licenses/gpl-2.0.html
   :alt: License: GPL-2
.. image:: https://travis-ci.org/acsone/acsone.buildbot.utils.svg?branch=master
   :target: https://travis-ci.org/acsone/acsone.buildbot.utils
.. image:: https://coveralls.io/repos/acsone/acsone.buildbot.utils/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/acsone/acsone.buildbot.utils?branch=master
A library providing some extensions to buildbot


Change Hook
===========

This module provide a change hook to process the payload of HTTP POST requests
from Planio. 
By default, it's not possible to register additional dialects in the
web_change_hoock than those natively provided by buildbot (a least with with
buildbot <= v0.8.12). To register the web hoock for planio you therefore need
to call `acsone.buildbot.status.change_hook.register_extendable_change_hook()`
This method can be used to register whatever you want as change hook.

  .. code::

    from acsone.buildbot.status.web.hook import planio
    from acsone.buildbot.status.change_hook import register_extendable_change_hook
    register_extendable_change_hook()
    
    ...
    
    c['status'].append(status.WebStatus(http_port=8010, allowForce=True,
    change_hook_dialects={
        'planio': {'mehod': planio.getChanges}))
