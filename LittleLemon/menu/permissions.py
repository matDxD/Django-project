from rest_framework import permissions

class IsGestor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Gestor').exists()

class IsDeliveryCrew(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Equipo de entrega').exists()

class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.groups.exists()  # El usuario no tiene grupo asignado
