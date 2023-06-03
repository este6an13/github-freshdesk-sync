import os
import requests
import sys

def get_github_user(username):
    headers = {
        'Authorization': f"Bearer {os.environ['GITHUB_TOKEN']}",
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(f"https://api.github.com/users/{username}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error retrieving GitHub user: {response.status_code} - {response.text}")
        return None


def search_freshdesk_contacts(email, subdomain):
    headers = {
        'Authorization': f"Bearer {os.environ['FRESHDESK_TOKEN']}",
        'Content-Type': 'application/json'
    }
    query = f"email:{email}"
    response = requests.get(f"https://{subdomain}.freshdesk.com/api/v2/search/contacts?query={query}", headers=headers)
    if response.status_code == 200:
        return response.json()
    # note: I'm assuming that we get 200 code with total field equal to 0 if we don't find results,
    # but I may be wrong, in which case, we should add a new condition here to let the client code know
    # that the user was not found
    else:
        print(f"Error searching Freshdesk contacts: {response.status_code} - {response.text}")
        return None


def create_freshdesk_contact(data, subdomain):
    headers = {
        'Authorization': f"Bearer {os.environ['FRESHDESK_TOKEN']}",
        'Content-Type': 'application/json'
    }
    response = requests.post("https://{subdomain}.freshdesk.com/api/v2/contacts", headers=headers, json=data)
    if response.status_code == 201:
        return response.json()
    else:
        print(f"Error creating Freshdesk contact: {response.status_code} - {response.text}")
        return None


def update_freshdesk_contact(contact_id, data, subdomain):
    headers = {
        'Authorization': f"Bearer {os.environ['FRESHDESK_TOKEN']}",
        'Content-Type': 'application/json'
    }
    response = requests.put(f"https://{subdomain}.freshdesk.com/api/v2/contacts/{contact_id}", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error updating Freshdesk contact: {response.status_code} - {response.text}")
        return None

def main():
    # Get command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python main.py <github_username> <freshdesk_subdomain>")
        return

    github_username = sys.argv[1]
    freshdesk_subdomain = sys.argv[2]

    # Retrieve the GitHub user information
    github_user = get_github_user(github_username)
    if github_user is None: # Error happened: user not found for example
        return

    # Extract required fields from GitHub user
    login = github_user.get('login')
    id_ = github_user.get('id') # we will use github id as user external id in freshdesk
    name = github_user.get('name')
    company = github_user.get('company')
    location = github_user.get('location')
    email = github_user.get('email')
    twitter_username = github_user.get('twitter_username')

    # Create or update contact in Freshdesk
    freshdesk_contacts = search_freshdesk_contacts(email, freshdesk_subdomain)
    if freshdesk_contacts is None: # Error happened
        return

    total_results = freshdesk_contacts.get('total')
    if total_results == 1: # we found the user in freshdesk
        # Contact found, update the contact
        contact_id = freshdesk_contacts.get('results')[0].get('id')
        data = {
            'name': name,
            'email': email, # this is the field that we will use for searching as it's unique in freshdesk
            # phone and mobile will be empty as we don't have those details
            'phone': '',
            'mobile': '',
            'twitter_id': twitter_username,
            'unique_external_id': str(id_),
            # our custom fields will be login, company and location took from github
            'custom_fields': {
                'github_login': login,
                'github_company': company,
                'github_location': location
            }
        }
        updated_contact = update_freshdesk_contact(contact_id, data, freshdesk_subdomain)
        if updated_contact is not None: # if None, error happened
            print("Contact updated successfully.")

    # I'm assuming that we get total = 0 if no results, but I may wrong, 
    # in which case we should modify the next elif condition and the search method implementation
    elif total_results == 0:
        # Contact not found, create a new contact
        data = {
            'name': name,
            'email': email, # this is the field that we will use for searching as it's unique in freshdesk
            # phone and mobile will be empty as we don't have those details
            'phone': '',
            'mobile': '',
            'twitter_id': twitter_username,
            'unique_external_id': str(id_),
            # our custom fields will be login, company and location took from github
            'custom_fields': {
                'github_login': login,
                'github_company': company,
                'github_location': location
            }
        }
        created_contact = create_freshdesk_contact(data, freshdesk_subdomain)
        if created_contact is not None: # if None, error happened
            print("Contact created successfully.")
    else:
        # Multiple contacts found, print an error
        # This should never happen as email is unique field in Freshdesk
        print("Error: Multiple contacts found with the same email.")

    # End of the program
    print("Program finished successfully.")

if __name__ == "__main__":
    main()
