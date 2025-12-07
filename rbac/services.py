from rbac.models import UserRole, RolePermission


def user_has_permission(user, permission_code):

    if user.is_superuser:
        return True

    roles = UserRole.objects.filter(user=user).values_list("role_id", flat=True)

    permissions = RolePermission.objects.filter(
        role_id__in=roles
    ).values_list("permission__code", flat=True)

    return permission_code in permissions
