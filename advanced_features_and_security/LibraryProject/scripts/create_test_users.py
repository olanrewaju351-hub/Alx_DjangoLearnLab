"""
Create three test users and add them to groups:
 - adminuser  -> Admins
 - editoruser -> Editors
 - vieweruser -> Viewers

Run with:
    python3 manage.py shell < scripts/create_test_users.py
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

def create_user_if_missing(username, password='pass1234'):
    user, created = User.objects.get_or_create(username=username)
    if created:
        user.set_password(password)
        user.save()
        print(f"Created user {username}")
    else:
        print(f"User {username} already exists")
    return user

def main():
    admin_group = Group.objects.get(name='Admins')
    editor_group = Group.objects.get(name='Editors')
    viewer_group = Group.objects.get(name='Viewers')

    # create users
    u_admin = create_user_if_missing('adminuser')
    u_editor = create_user_if_missing('editoruser')
    u_viewer = create_user_if_missing('vieweruser')

    # add to groups
    admin_group.user_set.add(u_admin)
    editor_group.user_set.add(u_editor)
    viewer_group.user_set.add(u_viewer)

    print("Assigned groups:")
    print(f" - adminuser groups: {[g.name for g in u_admin.groups.all()]}")
    print(f" - editoruser groups: {[g.name for g in u_editor.groups.all()]}")
    print(f" - vieweruser groups: {[g.name for g in u_viewer.groups.all()]}")

if __name__ == '__main__':
    main()
