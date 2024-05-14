import github, os
g = github.Github(login_or_token=os.environ["GITHUB_PAT"])

repo = g.get_repo("martezr/github-actions-tech-brief")

workflow_name = "dispatch.yml"
workflow = repo.get_workflow(workflow_name)

ref = repo.get_branch("main")
workflow.create_dispatch(ref=ref)