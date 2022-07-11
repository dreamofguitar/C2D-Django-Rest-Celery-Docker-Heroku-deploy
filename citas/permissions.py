from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = 'You must be the owner of this object'

    def has_object_permission(self, request, view, obj): 
        return obj.user == request.user 

class IsPatient(BasePermission):
    message = 'You must be a Patient'

    def has_permission(self, request, view):
        user = request.user 
        if user.client_type == 0:
            return True
        else:
            return False

class IsDoctor(BasePermission):
    message = 'You must be a Doctor'

    def has_permission(self, request, view):
        user = request.user 

        if user.client_type == 1:
            return True
        else:
            return False
                    
