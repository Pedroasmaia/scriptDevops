import requests as r
import base64
import json


with open("tfsec-report.json", "r") as f:
    report = json.load(f)

token_personal = '$(System.AccessToken)'
repo_id = '$(Build.Repository.ID)'
pullRequestId = '$(System.PullRequest.PullRequestId)'
project = '$(System.TeamProject)'
organization = 'seu_projeto'

authorization = str(base64.b64encode(bytes(':'+token_personal, 'ascii')), 'ascii')
headers = {
'Authorization': 'Basic '+authorization,
'Content-Type': 'application/json'
}
url_pr = f"https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repo_id}/pullRequests/{pullRequestId}/threads?api-version=7.1-preview.1"


if len(report['results']) != 0:
    for issue in report['results']:
        content = f"""
        # {issue['resource']} \n **Descrição:** {issue['description']} \n **Severidade:** {issue['severity']} \n **Arquivo:** {issue['location']['filename']}:{issue['location']['start_line']} \n **Resolução:** [{issue['resolution']}]({issue['links'][1]})
        """
        payload = {
        "comments": [
            {
            "parentCommentId": 0,
            "content": content,
            "commentType": "text",
            "visibility": {
                "value": "organization"
            }
            }
        ],
        "status": "active"
        }
        data = json.dumps(payload)
        comment_request = r.post(url_pr,data=data,headers=headers)