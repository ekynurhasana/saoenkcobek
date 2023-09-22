{
    'name': "HR Modifier",
    'summary': "Modifies HR Module",
    'description': "Modifies HR Module",
    'author': "Andini",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '1.1.1',
    'depends': ['base', 'hr', 'hr_attendance', 'hr_attendance_geolocation'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/hr_shift.xml',
        'views/hr_assign_work_time.xml',
    ],
    'installable': True,
    'application': True,
}
