# GitHub and Freshdesk Synchronization

This command line Python program retrieves information of a GitHub user and creates a new contact or updates an existing contact in Freshdesk using their respective APIs.

## Prerequisites

Before running the program, make sure you have the following:

- Python 3.x installed
- GitHub personal access token
- Freshdesk API key

## Installation

1. Clone the repository:

``` shell
git clone https://github.com/este6an13/github-freshdesk-sync.git
```

2. Change to the project directory

``` shell
cd github-freshdesk-sync
```

3. Install the required dependencies:
```shell
pip install -r requirements.txt
```

## Usage

To run the program, execute the following command:

```shell 
python main.py <github_username> <freshdesk_subdomain>
```

Replace <github_username> with the GitHub username for which you want to synchronize the information. Replace <freshdesk_subdomain> with the subdomain of your Freshdesk account.

Make sure to set the GitHub personal access token in the GITHUB_TOKEN environment variable and the Freshdesk API key in the FRESHDESK_TOKEN environment variable before running the program.

## Running the Tests

To run the unit tests, execute the following command:

``` shell
python -m unittest test.py
```

The tests will be executed, and the results will be displayed in the console.

Note: Make sure you have set the GitHub personal access token and Freshdesk API key in the respective environment variables before running the tests.