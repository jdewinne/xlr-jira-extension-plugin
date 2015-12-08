#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys
import com.xhaus.jyson.JysonCodec as json

ISSUES_RETREIVED_STATUS = 200

if jiraServer is None:
    print "No server provided."
    sys.exit(1)

if projectKey is None:
    print "No project key provided."
    sys.exit(1)

if version is None:
    print "No version provided."
    sys.exit(1)


content = """
{
    "jql":"project='%s' and fixVersion=%s and status not in (%s)"
}
""" % (projectKey, version, expectedStatus)


request = HttpRequest(jiraServer, username, password)

get_issues_url = '/rest/api/2/search'

response = request.post(get_issues_url, content, contentType = 'application/json')

# if response received from Jira
if response.getStatus() == ISSUES_RETREIVED_STATUS:
    # retrieve issue status
    issues = json.loads(response.getResponse())['issues']
    if len(issues) > 0:
        print "### One or more of your issues are not in a Completed or Resolved state.  Please ensure these JIRA issues are updated:"
        for issue in issues:
            print "\n* [%s](%s/browse/%s): %s" % (issue['key'],jiraServer['url'],issue['key'], issue['fields']['summary'])
        print "\n"
        sys.exit(1)
    else:
        print "### All issues are good."
else:
    print "Error from JIRA, HTTP Return: %s\n" % (response.getStatus())
    response.errorDump()
    sys.exit(1)
