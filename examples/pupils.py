from asq import query
from asq.selectors import k_

students = [dict(firstname='Joe', lastname='Blogs', scores=[56, 23, 21, 89]),
            dict(firstname='John', lastname='Doe', scores=[34, 12, 92, 93]),
            dict(firstname='Jane', lastname='Doe', scores=[33, 94, 91, 13]),
            dict(firstname='Ola', lastname='Nordmann', scores=[98, 23, 98, 87]),
            dict(firstname='Kari', lastname='Nordmann', scores=[86, 37, 88, 87]),
            dict(firstname='Mario', lastname='Rossi', scores=[37, 95, 45, 18])]

# Find all students where the first score is over 90
first_over_90 = query(students).where(lambda student: student['scores'][0] > 90)

# Select the last name of students where the first score is over 90
query(students).where(lambda student: student['scores'][0] > 90) \
               .select(lambda student: student['lastname'])

# Compute the maximum of all scores overall
query(students).select_many(lambda student: student['scores']).max()

# Order the students by last name and then by first name
query(students).order_by(lambda x: x['lastname']) \
               .then_by(lambda x: x['firstname'])


# It is very common to have selectors which retrieve a particular attribute
# from an object or index into the object using a particular key.  In these
# cases Python's lambda syntax can seem quite clunky.  To mitigate this, asq
# provides two factory functions called a_() and k_() which concisely generate
# selector functions for attributes and keys respectively.  The previous
# example could thus be rendered as::

query(students).order_by(k_('lastname')).then_by(k_('firstname'))
