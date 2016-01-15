# -*- coding: utf-8 -*-
# © 2016 ACSONE SA/NV
# License GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)

from buildbot.util import json
from dateutil.parser import parse as dateparse
from twisted.python import log
import logging

_HEADER_CT = 'Content-Type'
_CT_JSON = 'application/json'


def _get_payload(request):
    content = request.content.read()
    content_type = request.getHeader(_HEADER_CT)

    if content_type == 'application/json':
        payload = json.loads(content)
    elif content_type == 'application/x-www-form-urlencoded':
        payload = json.loads(request.args['payload'][0])
    else:
        raise ValueError('Unknown content type: %r' % (content_type,))

    log.msg("Payload: %r" % payload, logLevel=logging.DEBUG)

    return payload


def _process_change(payload, options):
    """
    Consumes the JSON as a python object and actually starts the build.

    :arguments:
        payload
            Python Object that represents the JSON sent by Planio Service
            Hook.
    """
    codebase = options.get('codebase', None)
    repo_url = payload['repository']['clone_url']
    # NOTE: what would be a reasonable value for project?
    # project = request.args.get('project', [''])[0]
    project = payload['repository']['full_name']
    changes = []
    if payload.get('deleted'):
        # log.msg("Branch `%s' deleted, ignoring" % branch)
        return changes

    for commit in payload['commits']:
        if not commit.get('distinct', True):
            log.msg('Commit `%s` is a non-distinct commit, ignoring...' %
                    (commit['id'],))
            continue

        files = []
        for kind in ('added', 'modified', 'removed'):
            files.extend(commit.get(kind, []))

        when_timestamp = dateparse(commit['timestamp'])

        log.msg("New revision: %s" % commit['id'][:8])

        change = {
            'author': '%s <%s>' % (commit['committer']['name'],
                                   commit['committer']['email']),
            'files': files,
            'comments': commit['message'],
            'revision': commit['id'],
            'when_timestamp': when_timestamp,
            # 'branch': branch,
            'revlink': commit['url'],
            'repository': repo_url,
            'project': project
        }

        if callable(codebase):
            change['codebase'] = codebase(payload)
        elif codebase is not None:
            change['codebase'] = codebase

        changes.append(change)

    return changes


def getChanges(request, options=None):
    """
    Reponds only to POST events and starts the build process

    :arguments:
        request
            the http request object
    """
    try:
        payload = _get_payload(request)
    except Exception, e:
        raise ValueError("Error loading JSON: " + str(e))
    changes = _process_change(payload, options or {})
    log.msg("Received %s changes from planio" % len(changes))
    return (changes, 'planio')
