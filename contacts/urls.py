from django.contrib import admin
from django.urls import path
from contacts.views import *

urlpatterns = [
    path('', ShowAll.as_view(), name='show all contacts'),

    path('new', AddNewPerson.as_view(), name='add new person'),
    path('modify/<int:person_id>', EditPerson.as_view(), name='modify person'),
    path('delete/<int:person_id>', DeletePerson.as_view(), name='delete person'),
    path('show/<int:person_id>', ShowDetails.as_view(), name='show details'),

    path('modify/<int:person_id>/addAddress', AddAddress.as_view()),
    path('modify/<int:person_id>/addExistingAddress', AddExistingAddress.as_view()),
    path('modify/<int:person_id>/addressDeleted', DeleteAddress.as_view()),
    path('modify/<int:person_id>/addToGroup', AddToGroup.as_view()),

    path('modify/<int:person_id>/addPhone', AddPhone.as_view()),
    path('modify/<int:person_id>/phoneDeleted', DeletePhone.as_view()),

    path('modify/<int:person_id>/addEmail', AddEmail.as_view()),
    path('modify/<int:person_id>/emailDeleted', DeleteEmail.as_view()),

    path('groups', ShowAllGroups.as_view(), name='show all groups'),
    path('new_group', AddNewGroup.as_view(), name='add new group'),
    path('modify_group/<int:group_id>', EditGroup.as_view(), name='modify group'),
    path('delete_group/<int:group_id>', DeleteGroup.as_view(), name='delete group'),
    path('show_group/<int:group_id>', ShowGroupDetails.as_view(), name='group details'),
]
