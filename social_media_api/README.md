Social Media API - accounts (README excerpt)
--------------------------------------------
Setup:
1. python3 -m venv venv && source venv/bin/activate
2. pip install -r requirements.txt  # include django, djangorestframework
3. python3 manage.py makemigrations
4. python3 manage.py migrate
5. python3 manage.py createsuperuser
6. python3 manage.py runserver

Endpoints:
- POST /api/accounts/register/   -> Register new user; returns token
- POST /api/accounts/login/      -> Login; returns token
- GET  /api/accounts/profile/    -> Get current user profile (Auth required)
- PUT  /api/accounts/profile/    -> Update profile (Auth required)
- POST /api/accounts/users/<username>/follow/ -> toggle follow (Auth required)

Auth:
- Use Token auth: set header "Authorization: Token <token_key>"

Posts & Comments API
--------------------
Base path: /api/

Posts:
- GET /api/posts/         -> list (supports ?search=, ?ordering=, pagination)
- POST /api/posts/        -> create (auth required)
- GET /api/posts/{id}/    -> retrieve (includes nested comments)
- PATCH/PUT /api/posts/{id}/ -> update (author only)
- DELETE /api/posts/{id}/ -> delete (author only)

Comments:
- GET /api/comments/      -> list
- POST /api/comments/     -> create (auth required; payload must include "post" id)
- GET /api/comments/{id}/
- PATCH/PUT /api/comments/{id}/ -> update (author only)
- DELETE /api/comments/{id}/ -> delete (author only)

Auth:
- Use Token auth: Add header "Authorization: Token <key>"

Follow & Feed
-------------
Endpoints (authenticated: include header "Authorization: Token <token>"):

- POST /api/accounts/follow/<user_id>/    -> follow a user
- POST /api/accounts/unfollow/<user_id>/  -> unfollow a user
- GET  /api/accounts/following/           -> list users you follow
- GET  /api/feed/                         -> paginated posts from users you follow (newest first)

Notes:
- A follow relationship is modeled via a many-to-many field: followers (related_name='following').
- Feed is paginated (default page_size=10). Use ?page=<n> to navigate.

