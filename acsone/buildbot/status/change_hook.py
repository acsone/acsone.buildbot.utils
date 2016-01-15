# -*- coding: utf-8 -*-
# © 2016 ACSONE SA/NV
# License GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)

import re

from buildbot.status.web.change_hook import ChangeHookResource
from twisted.python import log

original_getChanges = ChangeHookResource.getChanges


def getChanges(self, request):
    """
    Take the logic from the change hook, and then delegate it
    to the proper handler
    http://localhost/change_hook/DIALECT will load up
    buildmaster/status/web/hooks/DIALECT.py

    and call getChanges()

    the return value is a list of changes

    if DIALECT is unspecified, a sample implementation is provided
    if a callable is provided as value for the key 'method' in the dialect
    options this method will be called in place of getChanges()
    """
    uriRE = re.search(r'^/change_hook/?([a-zA-Z0-9_]*)', request.uri)

    if not uriRE:
        log.msg("URI doesn't match change_hook regex: %s" % request.uri)
        raise ValueError(
            "URI doesn't match change_hook regex: %s" % request.uri)

    changes = []
    src = None

    # Was there a dialect provided?
    if uriRE.group(1):
        dialect = uriRE.group(1)
    else:
        dialect = 'base'

    options = self.dialects.get(dialect) or {}
    method = options.get('method')
    if method:
        if not callable(method):
            m = ("The method specified '%s' must be a callable method "
                 "with 2 params: 'getChanges(requests, options=None)")
            m = m % method
            log.msg(m)
            raise ValueError(m)
        changes, src = method(request, options)
        log.msg("Got the following changes %s" % changes)
        self.request_dialect = dialect
        return (changes, src)
    return original_getChanges(self, request)


def register_extendable_change_hook():
    log.msg("Monkey patch buildbot.status.web.change_hook.ChangeHookResource"
            ".getChanges()")
    log.msg("Original method will be replaced by acsone.buildbot.status"
            ".change_hook.getChanges")
    log.msg("The purpose is to provide a way to register a callable to use to "
            "proces the request for a registered dialect")
    ChangeHookResource.getChanges = getChanges
