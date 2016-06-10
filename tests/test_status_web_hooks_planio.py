# -*- coding: utf-8 -*-
# © 2016 ACSONE SA/NV
# License GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)
import calendar
import mock
from StringIO import StringIO
from twisted.internet import defer
from twisted.trial import unittest
import buildbot.status.web.change_hook as change_hook
from buildbot.test.fake.web import FakeRequest

from acsone.buildbot.status.web.hook import planio
from acsone.buildbot.status.web.hook.planio import _HEADER_CT
from acsone.buildbot.status.web.hook.planio import _CT_JSON
from acsone.buildbot.status.change_hook import register_extendable_change_hook

# Sample Planio commit payload

gitJsonPayload = """
{
   "head_commit":{
      "committer":{
         "username":"lmi",
         "email":"laurent.mignon@acsone.e",
         "name":"Laurent Mignon"
      },
      "added":[
         "test.txt"
      ],
      "url":"https://acsone.plan.io/projects/sample_project/repository/228/revisions/1b253c6b9ccb348b5098a4954b143c2317ea8b68",
      "timestamp":"2016-01-15T12:00:43Z",
      "modified":[

      ],
      "message":"test.txt",
      "removed":[
      ],
      "id":"1b253c6b9ccb348b5098a4954b143c2317ea8b68"
   },
   "hostname":"acsone.plan.io",
   "repository":{
      "issues_url":"https://acsone.plan.io/projects/sample_project/issues.json",
      "name":"buildout",
      "url":"https://acsone.plan.io/projects/sample_project/repository/228",
      "html_url":"https://acsone.plan.io/projects/sample_project/repository/228",
      "clone_url":"git@acsone.plan.io:acsone-sample_project.buildout.git",
      "full_name":"sample_project.buildout",
      "id":228,
      "size":548842
   },
   "commits":[
      {
         "committer":{
            "username":"lmi",
            "email":"laurent.mignon@acsone.eu",
            "name":"Laurent Mignon"
         },
         "added":[
            "test.txt"
         ],
         "url":"https://acsone.plan.io/projects/sample_project/repository/228/revisions/1b253c6b9ccb348b5098a4954b143c2317ea8b68",
         "timestamp":"2016-01-15T12:00:43Z",
         "modified":[

         ],
         "message":"test.txt",
         "removed":[

         ],
         "id":"1b253c6b9ccb348b5098a4954b143c2317ea8b68"
      }
   ],
   "after":"1b253c6b9ccb348b5098a4954b143c2317ea8b68",
   "project":{
      "identifier":"sample_project",
      "name":"Odoo sample_project",
      "id":145
   },
   "before":"ea93241d2b51ff1ce7d7944c46f76cfcf432f7b1",
   "size":1,
   "ref": "refs/heads/master"
}
"""


class TestChangeHookConfiguredWithGitChange(unittest.TestCase):

    def setUp(self):
        register_extendable_change_hook()
        self.changeHook = change_hook.ChangeHookResource(
            dialects={'planio': {'method': planio.getChanges,
                                 'codebase': 'myCode'}})

    def check_changes(self, r, project='', codebase=None):
        self.assertEquals(len(self.request.addedChanges), 1)
        change = self.request.addedChanges[0]

        self.assertEquals(
            change["repository"],
            "git@acsone.plan.io:acsone-sample_project.buildout.git")
        self.assertEquals(
            calendar.timegm(change["when_timestamp"].utctimetuple()),
            1452859243
        )
        self.assertEquals(change["author"],
                          "Laurent Mignon <laurent.mignon@acsone.eu>")
        self.assertEquals(change["revision"],
                          '1b253c6b9ccb348b5098a4954b143c2317ea8b68')
        self.assertEquals(change["comments"], "test.txt")
        self.assertEquals(change["branch"], "master")
        self.assertEquals(
            change["revlink"],
            "https://acsone.plan.io/projects/sample_project/repository/228/"
            "revisions/1b253c6b9ccb348b5098a4954b143c2317ea8b68")

        self.assertEquals(change.get("project"), project)
        self.assertEquals(change.get("codebase"), codebase)

    # Test 'base' hook with attributes. We should get a json string
    # representing a Change object as a dictionary. All values show be set.
    @defer.inlineCallbacks
    def testGitWithChange(self):
        self.request = FakeRequest()
        self.request.content = StringIO(gitJsonPayload)
        self.request.received_headers[_HEADER_CT] = _CT_JSON
        self.request.uri = "/change_hook/planio"
        self.request.method = "POST"
        res = yield self.request.test_render(self.changeHook)
        self.check_changes(
            res, project="sample_project.buildout", codebase="myCode")
