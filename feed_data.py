import xlrd
import os
import django
django.setup()
from django.contrib.auth.models import User
from user_app.models import ExtraInfo, Designation, DepartmentInfo
from leave_application.models import LeavesCount
import user_app
django.setup()

class Data:

    def __init__(self, excel_file):
        self.file = xlrd.open_workbook(os.path.join(os.getcwd(), excel_file))
        self.staff_sheet = self.get_staff_sheet()
        self.faculty_sheet = self.get_faculty_sheet()

    def get_staff_sheet(self):
        return self.file.sheet_by_index(0)

    def get_faculty_sheet(self):
        return self.file.sheet_by_index(1)

    def get_designations(self):
        designation_staff = set([self.staff_sheet.cell(i, 3).value.strip() \
                                                        for i in range(1, 51)])
        designation_faculty = set([self.faculty_sheet.cell(i, 4).value.strip() \
                                                        for i in range(1, 64)])

        return list(designation_faculty | designation_staff)

    def get_departments(self):
        dept_staff = set(self.staff_sheet.cell(i, 4).value.strip() \
                                                     for i in range(1, 51))
        dept_faculty = set(self.faculty_sheet.cell(i, 3).value.strip() \
                                                     for i in range(1, 64))

        return list(dept_staff | dept_faculty)

    def create_users(self):

        for i in range(1, 51):
            try:
                email = self.get_unicode(self.staff_sheet.cell(i, 7))
                username = email.split('@')[0]
                print(username)
                name = self.get_unicode(self.staff_sheet.cell(i, 2)).split()
                first_name = name[1]
                last_name = " ".join(name[2:])
                sex = 'Male' if name[0]=='Mr.' else 'Female'
                unique_id = int(self.staff_sheet.cell(i, 1).value)
                designation = self.get_unicode(self.staff_sheet.cell(i, 3))
                print('designation: '+designation)

                # try:
                designation = Designation.objects.get(name=designation)
                # except:
                # Designation.objects.create(name=designation)
                designation = Designation.objects.get(name=designation)

                department = self.get_unicode(self.staff_sheet.cell(i, 4))
                print('department: '+department)
                # try:
                department = DepartmentInfo.objects.get(name=department)
                # except:
                    # DepartmentInfo.objects.create(name=department)
                    # department = DepartmentInfo.objects.get(name=department)

                user_type = 'staff'
                sanc_auth = self.get_unicode(self.staff_sheet.cell(i, 5))
                sanc_auth = Designation.objects.get(name=sanc_auth)
                sanc_officer = self.get_unicode(self.staff_sheet.cell(i, 6))
                sanc_officer = Designation.objects.get(name=sanc_officer)

                u = User.objects.create_user(
                    username = username,
                    password = 'hello123',
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                )

                u.extrainfo.sex = sex
                u.extrainfo.unique_id = unique_id
                u.extrainfo.department = department
                u.extrainfo.user_type = user_type
                u.extrainfo.designation = designation
                u.extrainfo.sanctioning_authority = sanc_auth
                u.extrainfo.sanctioning_officer = sanc_officer
                u.extrainfo.aboutme = 'hello I am'+first_name

                u.extrainfo.save()
                LeavesCount.objects.create(user=u)
            except Exception as e:
                print(e)



        for i in range(1, 64):
            try:
                email = self.get_unicode(self.faculty_sheet.cell(i, 7))
                username = email.split('@')[0]
                print(username)
                name = self.get_unicode(self.faculty_sheet.cell(i, 2)).split()
                first_name = name[1]
                last_name = " ".join(name[2:])
                sex = 'Male' if name[0]=='Mr.' else 'Female'
                unique_id = int(self.faculty_sheet.cell(i, 1).value)
                designation = self.get_unicode(self.faculty_sheet.cell(i, 4))
                print('designation: '+designation)
                designation = Designation.objects.get(name=designation)
                department = self.get_unicode(self.faculty_sheet.cell(i, 3))
                print('department: '+department)
                department = DepartmentInfo.objects.get(name=department)
                user_type = 'faculty'
                sanc_auth = self.get_unicode(self.faculty_sheet.cell(i, 5))
                sanc_auth = Designation.objects.get(name=sanc_auth)
                sanc_officer = self.get_unicode(self.faculty_sheet.cell(i, 6))
                sanc_officer = Designation.objects.get(name=sanc_officer)

                u = User.objects.create_user(
                    username = username,
                    password = 'hello123',
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                )

                u.extrainfo.sex = sex
                u.extrainfo.unique_id = unique_id
                u.extrainfo.department = department
                u.extrainfo.user_type = user_type
                u.extrainfo.sanctioning_authority = sanc_auth
                u.extrainfo.sanctioning_officer = sanc_officer
                u.extrainfo.aboutme = 'hello I am'+first_name
                u.extrainfo.designation = designation

                u.extrainfo.save()
                LeavesCount.objects.create(user=u)
            except Exception as e:
                print(e)
                

    def get_unicode(self, string):
        return string.value.strip()

    def create_designations(self, lst):
        for designation in lst:
            Designation.objects.create(name=designation)

    def create_departments(self, lst):
        # map(lambda x: DepartmentInfo.objects.create(name=x), lst)
        for dept in lst:
            DepartmentInfo.objects.create(name=dept)


# if __name__ == '__main__':
#     # django.settings.configure()
#     data = Data('data.xlsx')
#     data.create_designations(data.get_departments())
#     data.create_departments(data.get_departments())
#     data.create_users()


"""
from feed_data import Data; data = Data('data.xlsx'); data.create_users();
data.create_designations(data.get_designations())
"""
