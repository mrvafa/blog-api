# Blog API

This is django project that uses API to set up a restfull api blog. In the blog, users can create an account and authors
can post articles.

## Table of content

1. [Installation](#installation)
2. [Usage examples](#usage-examples)
3. [TODO](#todo)

<a name="installation"></a>
## Installation

- Clone the repository.
- Create virtual environment using `python -m virtualenv --python=python3 env`.
- Activate env (in linux use `. env/bin/activate`).
- Install requirements.txt using `pip install -r requirements.txt`.
- Create .env file (`cp .env.template .env`).
- Fill the `.env` file.

<a name="usage-examples"></a>
## Usage examples
Not ready!!

<a name="todo"></a>
## TODO
- [X] Start & setup project.
- [X] Create custom user model.
- [X] Create test for user model.
- [X] Install django allauth, rest-api and set urls.
- [X] Create email for user (console base).
- [X] Set login with both email and username
- [X] Create position for profile.
- [X] Create tag app and model.
- [X] Create post app and model.
- [X] Create API for post (list, single, add, edit and remove).
- [X] Create API for tag (list, single, add, edit and remove).
- [X] Customize API for editing post and tag. (Change post's and tag's image, and remove tag's image.) 
- [X] Add user to post's model and add to API.
- [X] Create custom authorization AllowAuthor.
- [X] Override RetrieveUpdateAPIView for use previous data if edit data is empty.
- [X] Create position and post, many to many fields.
- [X] Merged User and Profile.
- [X] Create Profile API.