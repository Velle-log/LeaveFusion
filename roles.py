import xlsxwriter as xls

from django.contrib.auth.models import User

workbook = xls.Workbook('Roles_for_testing.xlsx')
bold = workbook.add_format({'bold': True, 'align': 'right'})
al_right = workbook.add_format({'align': 'right'})
worksheet = workbook.add_worksheet()
worksheet.set_column(1, 2, 40)
# worksheet.set_row(1, 90, 1)

worksheet.write(0, 0, 'S. No.', bold)
worksheet.write(0, 1, 'Role of', bold)
worksheet.write(0, 2, 'Played by', bold)


with open('emails', 'r') as f:
    count = 1
    for user in User.objects.all():
        if user.username == 'saket':
            continue
        email = f.readline().strip()
        if not email:
            break
        worksheet.write(count, 0, count, al_right)
        worksheet.write(count, 1, "{} {}".format(user.first_name, user.last_name), al_right)
        worksheet.write(count, 2, email, al_right)
        user.email = email
        user.save()
        count += 1
workbook.close()
