import time

import requests

def fetch_github_data(data, token):
    # Collect unique languages from the data
    languages = set(fw['programmingLanguage'] for fw in data.get('frameworks', []))
    print(f"Processing {len(languages)} unique programming languages")

    processed_languages = {}
    for language in languages:
        topic_name = language.lower()
        language_data = fetch_data(topic_name, token)
        if language_data:
            processed_languages[language] = language_data

    return processed_languages

def fetch_data(topic_name, token):
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {token}"
    }

    url = f"https://api.github.com/search/topics?q={topic_name}"
    url_repos = f"https://api.github.com/search/repositories?q=topic:{topic_name}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        time.sleep(2)

        response_repos = requests.get(url_repos, headers=headers)
        response_repos.raise_for_status()
        data_repos = response_repos.json()

        if not data.get('items'):
            print(f"No results found for topic: {topic_name}")
            return None

        if not data_repos.get('items'):
            print(f"No repositories found for topic: {topic_name}")
            return None

        first_item = data['items'][0]
        related_repos = []

        if first_item.get('name') == topic_name:
            for repo in data_repos['items']:
                repo = {
                    'name': repo.get('name', 'N/A'),
                    'description': repo.get('description', 'N/A'),
                    'watchers': repo.get('watchers_count', 'N/A'),
                    'url': repo.get('html_url', 'N/A')
                }
                related_repos.append(repo)

            topic_info = {
                key: value for key, value in {
                'description': first_item.get('description', 'N/A'),
                'created_by': first_item.get('created_by', 'N/A'),
                'released': first_item.get('released', 'N/A'),
                'related_repos': related_repos
                }.items() if value != 'N/A' or value != []
            }
            print(f"- Processed topic: {topic_name}")
            return topic_info
        else:
            print(f"-! Invalid topic: {topic_name}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None