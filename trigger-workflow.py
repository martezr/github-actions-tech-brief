import github, os
import time
from morpheuscypher import Cypher
import requests


def trigger_workflow(workflow, ref, data):
    print(workflow.create_dispatch(ref=ref,inputs=data))
    time.sleep(15)
    id = workflow.get_runs()[0].id
    print(workflow.get_runs()[0].status)
    return id
    #for run in workflow.get_runs():
    #    print(run.id)
    #    print(run.run_started_at)
    #    print(run.status)
    #    print(run.event)
        # Wait for the catalog item details to populate
    #    time.sleep(15)

def poll_workflow_execution(workflow, id):
    status = "in_progress"

    while status == "in_progress" or status == "queued":
        for run in workflow.get_runs():
            if run.id == id:
                status = run.status
                print("current status: " + status )
                print("logs: " + run.logs_url)
                code, headers, data = workflow._requester.requestJson("GET", run.logs_url)
                print("code: " + str(code))
                print(headers)
                print("data: " + data)
                if code == 302:
                    print("location: " + headers['location'])
                    r = requests.get(headers['location'])
                    with open('/tmp/logs.zip', 'wb') as out:
                        out.write(r.content)
        time.sleep(30)

    return status
    
def main():
    githubToken = Cypher(morpheus=morpheus,ssl_verify=False).get('secret/ghtoken')
    g = github.Github(login_or_token=githubToken)

    repo = g.get_repo("martezr/github-actions-tech-brief")

    workflow_name = "dispatch.yml"
    workflow = repo.get_workflow(workflow_name)

    data = {}
    data['print_tags'] = True
    data['tags'] = "test"

    ref = repo.get_branch("main")
    id = trigger_workflow(workflow, ref, data)
    poll_workflow_execution(workflow, id)

if __name__ == "__main__":
    main()