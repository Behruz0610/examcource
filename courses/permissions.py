from rest_framework import permissions
from rest_framework.permissions import BasePermission
import datetime

# 1) Premium courselarni faqat adminlar ko'ra oladi
class IsAdminForPremiumCourse(BasePermission):
    def has_permission(self, request, view):
        # Faqat adminlar (is_staff) uchun ruxsat
        return request.user and request.user.is_staff

# 2) Faqat juft yillar uchun ruxsat
class IsEvenYear(BasePermission):
    def has_permission(self, request, view):
        year = datetime.datetime.now().year
        return year % 2 == 0

# 3) Faqat is_superuser=True foydalanuvchilar kira oladi
class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

# 4) Faqat PUT va PATCH ruxsat, qolganlari blok
class PutPatchOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in ['PUT', 'PATCH']