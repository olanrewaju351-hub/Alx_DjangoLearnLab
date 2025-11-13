Permissions & Groups Setup
--------------------------
- Model: bookshelf.Book defines custom permissions:
  - can_view, can_create, can_edit, can_delete

- Groups created:
  - Admins: can_view, can_create, can_edit, can_delete
  - Editors: can_view, can_create, can_edit
  - Viewers: can_view

How to modify groups/permissions:
- Use Django admin (Auth -> Groups) OR run the provided shell script (see project root scripts/create_groups.sh)

How to check permissions:
- In code: request.user.has_perm('bookshelf.can_edit')
- In shell: User.objects.get(username='...').has_perm('bookshelf.can_edit')

Protect views:
- Use @permission_required('bookshelf.can_edit', raise_exception=True)

