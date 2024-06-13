import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

gitlab_host = 'https://gitlab.example.com'
token = os.getenv('GITLAB_TOKEN')

def get_all_project_ids():
    project_ids = []
    try:
        page = 1
        while True:
            projects_url = f"{gitlab_host}/api/v4/projects?private_token={token}&per_page=100&page={page}"
            projects_response = requests.get(projects_url)
            projects = projects_response.json()
            if not projects:
                break
            for project in projects:
                project_ids.append(project['id'])
            page += 1
    except Exception as error:
        print(f"Error fetching projects: {error}")
    return project_ids

def delete_project_artifacts(project_id):
    try:
        artifacts_url = f"{gitlab_host}/api/v4/projects/{project_id}/artifacts?private_token={token}"
        response = requests.delete(artifacts_url)
        if response.status_code == 204:
            print(f"All artifacts for project {project_id} deleted successfully.")
        else:
            print(f"Failed to delete artifacts for project {project_id}. Status code: {response.status_code}")
    except Exception as error:
        print(f"Error deleting artifacts for project {project_id}: {error}")

def delete_project_job_artifacts(project_id):
    try:
        page = 1
        while True:
            jobs_url = f"{gitlab_host}/api/v4/projects/{project_id}/jobs?private_token={token}&per_page=100&page={page}"
            jobs_response = requests.get(jobs_url)
            jobs = jobs_response.json()
            if not jobs:
                break
            for job in jobs:
                try:
                    job_artifacts_url = f"{gitlab_host}/api/v4/projects/{project_id}/jobs/{job['id']}/artifacts?private_token={token}"
                    response = requests.delete(job_artifacts_url)
                    if response.status_code == 204:
                        print(f"All artifacts for job {job['id']} in project {project_id} deleted successfully.")
                    else:
                        print(f"Failed to delete artifacts for job {job['id']} in project {project_id}. Status code: {response.status_code}")
                except Exception as error:
                    print(f"Error deleting artifacts for job {job['id']} in project {project_id}: {error}")
            page += 1
    except Exception as error:
        print(f"Error deleting job artifacts for project {project_id}: {error}")

# Example usage
if __name__ == "__main__":
    project_ids = get_all_project_ids()
    for project_id in project_ids:
        delete_project_artifacts(project_id)
        delete_project_job_artifacts(project_id)
