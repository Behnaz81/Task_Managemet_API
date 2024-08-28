from rest_framework import permissions


class IsManeger(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'manager'
    

class IsTeamLeader(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teamleader'
    

class IsTeamMember(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teammember'
    