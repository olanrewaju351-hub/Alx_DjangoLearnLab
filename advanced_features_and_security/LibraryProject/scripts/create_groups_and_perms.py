"""
Create groups and assign custom permissions for the `bookshelf.Book` model.

Run with:
    python3 manage.py shell < scripts/create_groups_and_perms.py
"""
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

def main():
    # Create groups
    admin_group, _  = Group.objects.get_or_create(name='Admins')
    editor_group, _ = Group.objects.get_or_create(name='Editors')
    viewer_group, _ = Group.objects.get_or_create(name='Viewers')

    # Get content type for Book
    ct = ContentType.objects.get_for_model(Book)

    # Get (or create) permissions by codename
    def get_perm(codename, name):
        perm, created = Permission.objects.get_or_create(
            codename=codename,
            content_type=ct,
            defaults={'name': name}
        )
        return perm

    p_view   = get_perm('can_view', 'Can view book')
    p_create = get_perm('can_create', 'Can create book')
    p_edit   = get_perm('can_edit', 'Can edit book')
    p_delete = get_perm('can_delete', 'Can delete book')

    # Assign perms to groups
    admin_group.permissions.set([p_view, p_create, p_edit, p_delete])
    editor_group.permissions.set([p_view, p_create, p_edit])
    viewer_group.permissions.set([p_view])

    print("Groups created/updated:")
    for g in (admin_group, editor_group, viewer_group):
        print(f" - {g.name}: {[p.codename for p in g.permissions.all()]}")

if __name__ == '__main__':
    main()
