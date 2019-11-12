from django.shortcuts import render, redirect
from django.views import View
from contacts.models import *


class ShowAll(View):
    def get(self, request):
        persons = Person.objects.all().order_by('name')
        person_list = "".join([f'<tr><td><a href ="show/{person.id}">{person.name} {person.surname}</a></td>'
                               f'<td><a href="modify/{person.id}">edit</a> | '
                               f'<a href="delete/{person.id}">delete</a></td></tr>'
                               for person in persons])
        return render(request, 'index.html', context={'person_list': person_list})


class AddNewPerson(View):
    def get(self, request):
        return render(request, 'add_person.html', context={'info': 'Add your new contact'})

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        if request.POST.get('description') == '':
            description = '-'
        else:
            description = request.POST.get('description')
        new_person = Person.objects.create(name=name, surname=surname, description=request.POST.get('description'))
        ctx = {'info': 'New contact:',
               'name': new_person.name,
               'surname': new_person.surname,
               'description': description
               }
        return render(request, 'add_person_ok.html', context=ctx)


class EditPerson(View):
    def get(self, request, person_id):
        person = Person.objects.get(id=person_id)

        all_addresses = Address.objects.all()
        address_options = "".join([f'<option value="{address.id}">'
                                   f'{address.street} {address.house}/{address.flat}, {address.city}</option>'
                                   for address in all_addresses])

        person_address = Address.objects.filter(id=person.address_id)
        address = "".join([f'{p_address.city}<br>'
                           f'{p_address.street} {p_address.house}/{p_address.flat}' for p_address in person_address])

        phones = Phone.objects.filter(person_id=person_id)
        phone_list = "".join([f'<option value="{phone.id}">{phone.phone_number} ({phone.type})</option>'
                              for phone in phones])

        emails = Email.objects.filter(person_id=person_id)
        email_list = "".join([f'<option value="{email.id}">{email.email} ({email.type})</option>' for email in emails])

        groups = Group.objects.all()
        group_options = "".join([f'<option value="{group.id}">{group.name}</option>' for group in groups])

        ctx = {'info': 'Change contact details',
               'name': person.name,
               'surname': person.surname,
               'description': person.description,
               'person_id': person.id,
               'address_options': address_options,
               'address': address,
               'phone_options': phone_list,
               'email_options': email_list,
               'group_options': group_options
               }
        return render(request, 'edit_person.html', context=ctx)

    def post(self, request, person_id):
        person = Person.objects.get(id=person_id)
        person.name = request.POST.get('name')
        person.surname = request.POST.get('surname')
        person.description = request.POST.get('description')
        person.save()
        ctx = {'info': 'Contact changed, new details:',
               'name': person.name,
               'surname': person.surname,
               'description': person.description}
        return render(request, 'edit_person_ok.html', context=ctx)


class DeletePerson(View):
    def get(self, request, person_id):
        person = Person.objects.get(id=person_id)
        ctx = {'info': f'Do you want to delete {person.name} {person.surname} from your contact box?'}
        return render(request, 'delete_person.html', context=ctx)

    def post(self, request, person_id):
        person = Person.objects.get(id=person_id)
        if request.POST.get('delete') == 'Yes':
            person.delete()
            return render(request, 'delete_person_ok.html', context={'info': 'Contact deleted.'})
        return redirect('/')


class AddAddress(View):
    def post(self, request, person_id):
        person = Person.objects.get(id=person_id)
        city = request.POST.get('city')
        street = request.POST.get('street')
        house_number = request.POST.get('house_number')
        if request.POST.get('flat_number') != '':
            flat_number = request.POST.get('flat_number')
            new_address = Address.objects.create(city=city, street=street, house=house_number, flat=flat_number)
            person.address_id = new_address.id
            person.save()
        else:
            new_address = Address.objects.create(city=city, street=street, house=house_number)
            person.address_id = new_address.id
            person.save()
        ctx = {'info': 'Address added to the contact',
               'person_id': person_id}
        return render(request, 'edit_person_add_else.html', context=ctx)


class AddExistingAddress(View):
    def post(self, request, person_id):
        person = Person.objects.get(id=person_id)
        address_id = request.POST.get('address_list')
        new_address = Address.objects.get(id=address_id)
        person.address_id = new_address.id
        person.save()
        ctx = {'info': 'Address added to the contact',
               'person_id': person_id}
        return render(request, 'edit_person_add_else.html', context=ctx)


class DeleteAddress(View):
    def post(self, request, person_id):
        person = Person.objects.get(id=person_id)
        if request.POST.get('delete_address') != '':
            person.address_id = ''
            person.save()
        ctx = {'info': 'Address deleted.'}
        return render(request, 'edit_person_deleted.html', context=ctx)


class AddPhone(View):
    def post(self, request, person_id):
        phone_number = request.POST.get('phone_number')
        phone_type = request.POST.get('phone_type')
        new_phone_number = Phone.objects.create(phone_number=phone_number, type=phone_type, person_id=person_id)
        ctx = {'info': f'Phone number added to the contact: {new_phone_number.phone_number}',
               'person_id': person_id}
        return render(request, 'edit_person_add_else.html', context=ctx)


class DeletePhone(View):
    def post(self, request, person_id):
        phone_id = request.POST.get('phone_list')
        phone_to_delete = Phone.objects.get(id=phone_id)
        phone_to_delete.delete()
        ctx = {'info': 'Phone number deleted.'}
        return render(request, 'edit_person_deleted.html', context=ctx)


class AddEmail(View):
    def post(self, request, person_id):
        email = request.POST.get('email')
        email_type = request.POST.get('email_type')
        new_email = Email.objects.create(email=email, type=email_type, person_id=person_id)
        ctx = {'info': f'E-mail added to the contact: {new_email.email}',
               'person_id': person_id}
        return render(request, 'edit_person_add_else.html', context=ctx)


class DeleteEmail(View):
    def post(self, request, person_id):
        email_id = request.POST.get('email_list')
        email_to_delete = Email.objects.get(id=email_id)
        email_to_delete.delete()
        ctx = {'info': 'E-mail deleted.'}
        return render(request, 'edit_person_deleted.html', context=ctx)


class ShowDetails(View):
    def get(self, request, person_id):
        person = Person.objects.get(id=person_id)
        addresses = Address.objects.filter(id=person.address_id)
        phones = Phone.objects.filter(person_id=person_id)
        emails = Email.objects.filter(person_id=person_id)
        address_list = "".join([f'{address.city}<br>{address.street} {address.house}/{address.flat}'
                                for address in addresses])
        phone_list = "".join([f'<li>{phone.phone_number} ({phone.type})</li>' for phone in phones])
        email_list = "".join([f'<li>{email.email} ({email.type})</li>' for email in emails])
        groups = person.group.all()
        group_list = "".join([f"<li>{group.name}</li>" for group in groups])

        ctx = {'info': 'Contact details',
               'name_and_surname': f'{person.name} {person.surname}',
               'description': person.description,
               'address': address_list,
               'phone': phone_list,
               'email': email_list,
               'person_id': person.id,
               'group_list': group_list
               }
        return render(request, 'show_details.html', context=ctx)


class ShowAllGroups(View):
    def get(self, request):
        groups = Group.objects.all().order_by('name')
        group_list = "".join([f'<tr><td><a href ="show_group/{group.id}">{group.name}</a></td>'
                               f'<td><a href="modify_group/{group.id}">edit</a> | '
                               f'<a href="delete_group/{group.id}">delete</a></td></tr>'
                               for group in groups])
        return render(request, 'group_index.html', context={'group_list': group_list})


class AddNewGroup(View):
    def get(self, request):
        return render(request, 'add_group.html', context={'info': 'Add your new group'})

    def post(self, request):
        name = request.POST.get('name')
        new_group = Group.objects.create(name=name)
        ctx = {'info': 'New group',
               'name': new_group.name,
               }
        return render(request, 'add_group_ok.html', context=ctx)


class ShowGroupDetails(View):
    def get(self, request, group_id):
        group = Group.objects.get(id=group_id)
        all_persons = group.person_set.all()
        members = "".join([f'<li>{person.name} {person.surname}</li>' for person in all_persons])
        ctx = {'info': 'Group details',
               'name': group.name,
               'members': members,
               'group_id': group_id
               }
        return render(request, 'show_group_details.html', context=ctx)


class EditGroup(View):
    def get(self, request, group_id):
        group = Group.objects.get(id=group_id)
        ctx = {'info': 'Change group name',
               'name': group.name
               }
        return render(request, 'edit_group.html', context=ctx)

    def post(self, request, group_id):
        group = Group.objects.get(id=group_id)
        new_name = request.POST.get('name')
        group.name = new_name
        group.save()
        ctx = {'info': "Group's name changed",
               'name': group.name
               }
        return render(request, 'edit_group_ok.html', context=ctx)


class DeleteGroup(View):
    def get(self, request, group_id):
        group = Group.objects.get(id=group_id)
        ctx = {'info': f'Do you want to delete {group.name}?'}
        return render(request, 'delete_group.html', context=ctx)

    def post(self, request, group_id):
        group = Group.objects.get(id=group_id)
        if request.POST.get('delete') == 'Yes':
            group.delete()
            return render(request, 'delete_group_ok.html', context={'info': 'Group deleted.'})
        return redirect('/groups')


class AddToGroup(View):
    def post(self, request, person_id):
        person = Person.objects.get(id=person_id)
        group_id = request.POST.get('group_list')
        group = Group.objects.get(id=group_id)
        person.group.add(group)
        ctx = {'info': 'Contact added to the group',
               'person_id': person_id}
        return render(request, 'edit_person_add_else.html', context=ctx)
