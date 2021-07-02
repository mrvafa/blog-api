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

|METHOD|             url                 | fields|   respond   |headers|description|
|------|---------------------------------|----------------|---------| --- |---|
| POST | /register/  | username, email, password1, password2 |detail| None|Create user|
| POST | /password/reset/  | email| detail | None |Reset user password|
| POST | /password/reset/confirm/  | new_password1, new_password2, uid, token| detail| None|Change user password after resting `/password/reset/`|
| POST | /login/  | (Username or email), password| key | None |Change user password after resting|
| GET & PATCH & PUT | /profile/  | None or (username, first_name, last_name)| pk, username, first_name, last_name, email | Token |Get user info and change some data|
| POST | /account-confirm-email/(?P<key>[-:\w]+)/ | key| key| None | Confirm email |
| GET | /post/api/ | None |`<list-of-posts>`| None| List of posts|
| GET | /post/api/s/<str:slug>/ | None | id, title, slug, body, tags, image, added_datetime modify_datetime |None |  Detail post by `slug`|
| PATCH | /post/api/s/<str:slug>/edit/ | title, body, tags, image|id, title, slug, body, tags, image, added_datetime modify_datetime | Token (Author of post) |  Edit post with `slug`|
| DELETE | /post/api/s/<str:slug>/destroy/ | Token (Author of post or Admin)| None | Token (Author of post or admin) |  Delete post by `slug`|
| POST | /post/create/ | title, body, tags, image|id, title, slug, body, tags, image, added_datetime modify_datetime | Token (Author)| Create post|
| GET | /tag/api/ | None | <list-of-tags> | None | List of tags|
| GET | /tag/api/s/<str:slug>/ | None | id, title, slug, body, image, added_datetime modify_datetime | None |  Detail of tag `slug`|
| PATCH | /tag/api/s/<str:slug>/edit/ | title, body, image | id, title, slug, body, image, added_datetime modify_datetime | Token (Author) |  Edit tag by `slug`|
| DELETE | /tag/api/s/<str:slug>/destroy/ |None | None | Token (Admin) |  Delete tag by `slug`|
| POST | /tag/create/ | title, image, body | id, title, slug, body, image, added_datetime modify_datetime|Token (Author) | Create tag|
| GET | /profile/api/private/ | None | `<list-of-users>` |Token (Admin) | list of all users|
| GET | /profile/api/private/<int:pk>/ | None| id, last_login, is_superuser, username, first_name, last_name, is_staff, is_active, date_joined, email, gender, birthday, phone_number, image, groups, user_permissions | Token (Admin) | detail of user by `pk`|
| DELETE | /profile/api/private/<int:pk>/destroy/ | None| None | Token (Admin) | delete user by `pk`|
| GET | /profile/api/authors/ | None|  `<list-of-authors>` | None | get all authors|
| GET | /profile/api/u/<str:username>/ | None | username, image, posts, birthday, gender | None | get author by `username`|
| GET & PATCH & PUT | /profile/api/edit-account/ | username, first_name, last_name, birthday, gender| username, first_name, last_name, birthday, gender, email , password | Token | edit account|
| DELETE | /profile/api/delete-account/ | None | None | Token | delete account |
| PUT | /profile/api/change-password/ | new_password1, new_password2 | None | Token | Change password |
| POST | /profile/api/send-sms/ | phone_number | None | Token | send sms to phone_number |
| PUT | /profile/api/set-phone-number/ | phone_number, code | None | Token | set phone_number if code is right |
| PUT | /profile/api/<int:pk>/change-user-author/ | is_author | None | Token (Admin) | change user author permission |
| PUT | /profile/api/<int:pk>/change-user-permissions/ | is_admin, is_active, is_staff | is_admin, is_active, is_staff | Token (Admin) | set phone_number if code is right |

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
- [X] Create API for user to make user admin, author, non-admin, non-author and deactivate-user.
- [X] Create custom permission for post (is_author)
- [X] Remove phone_validation, create function to set phone number.
- [X] Add phone_number_conform table (requested_time, expired_time, code, phone_number)
- [X] Add Author page and Tag page (get all posts by author/tag).
- [X] Tests
- [X] Search and search filtering
- [X] Ordering Posts, authors and tags
- [X] Finishing version 1.0
- [ ] Create search history for user
- [ ] Use `phonenumbers` package for phone number validations
- [ ] Add likes, read_later, views, read
- [ ] Add read time estimate.
- [ ] Add comments (self-relation, like and dislike)
- [ ] Add message (contains text, sender, receiver, time, read?)
- [ ] Block user
- [ ] Follow user
- [ ] Resend email
- [ ] Captcha