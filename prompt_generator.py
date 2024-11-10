import requests


def generator(input):
    # Replace with your actual API key and external user ID
    api_key = 'gSmlY5VaDlop0SJAS9jHid2PaAsEKgFV'
    external_user_id = '<replace_external_user_id>'
    # Create Chat Session
    create_session_url = 'https://api.on-demand.io/chat/v1/sessions'
    create_session_headers = {
        'apikey': api_key
    }
    create_session_body = {
        "pluginIds": [],
        "externalUserId": external_user_id
    }
    # Make the request to create a chat session
    response = requests.post(create_session_url, headers=create_session_headers, json=create_session_body)
    response_data = response.json()
    # Extract session ID from the response
    session_id = response_data['data']['id']
    # Submit Query
    submit_query_url = f'https://api.on-demand.io/chat/v1/sessions/{session_id}/query'
    submit_query_headers = {
        'apikey': api_key
    }
    submit_query_body = {
        "endpointId": "predefined-openai-gpt4o",
        "query": f"Create a casual informal conversation starter for the name {input}",
        "pluginIds": ["plugin-1712327325", "plugin-1713962163"],
        "responseMode": "sync"
    }
    # Make the request to submit a query
    query_response = requests.post(submit_query_url, headers=submit_query_headers, json=submit_query_body)
    query_response_data = query_response.json()
    query_response_data = json.loads(query_response_data)
    return query_response_data

print(generator("Scott"))