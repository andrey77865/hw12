import pickle
import re

from collections import UserDict
from datetime import date, datetime


class AddressBook(UserDict):
    def __init__(self):
        self.data = {}

    def add_record(self, rec):
        self.data.update(Record.add(rec))

    def iterator(self, n):
        result_list = list(self.data.items())
        contacts_count = len(self.data)
        while True:
            if n <= contacts_count:
                yield result_list[:n]
            else:
                yield result_list[:contacts_count]

    def find(self, searchable):

        for key, value in self.data.items():

            if key.rfind(searchable) >= 0:  # Search by key (name)
                print(
                    f'Search by {searchable}": {value.name}, {value.phones}, {value.bday}')

            else:

                for phone in value.phones:  # Search by value (phone)

                    if phone.value.rfind(searchable) >= 0:
                        print(
                            f'Search by {searchable}": {value.name}, {value.phones}, {value.bday}')

    def save(self):
        with open("data.bin", "wb") as file:
            pickle.dump(self, file)

    def load(self):
        with open("data.bin", "rb") as file:
            backup = pickle.load(file)

        return backup


class Field:
    pass


class Name(Field):
    def __init__(self, name):
        self.value = name

    def __repr__(self):
        return f"Name: {self.value}"


class Phone(Field):
    def __init__(self, phone=None):
        self.__value = None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, phone):
        phone = re.sub('\W+', '', phone)
        check_phone = re.match(
            r"([0-9]{3}[0-9]{3}[0-9]{2}[0-9]{2}$)", phone)

        if not check_phone:
            raise ValueError(
                "Incorrect phone number format (+380xxxxxxxxx")

        if phone.startswith("0"):
            phone = "+38" + phone
        elif phone.startswith("380"):
            phone = "+" + phone

        self.__value = phone

    def __repr__(self):
        return f"{self.value}"


class Birthday(Field):
    def __init__(self, bday=None):
        self.__value = None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, bday):
        try:
            datetime_obj = datetime.strptime(bday, "%d-%m-%Y")
        except ValueError:
            print("Incorrect birthday format (dd-mm-yyyy)")
        else:
            self.__value = datetime_obj.date()

    def __repr__(self):
        return f"Birthday date: {self.value}"


class Record():
    def __init__(self, name: Name, phone: Phone = None, bday: Birthday = None):
        self.name = name
        self.phones = []
        if phone.value:
            self.phones.append(phone)
        self.bday = bday

    def days_to_birthday(self):
        if self.bday.value != None:
            today = date.today()
            next_bday = self.bday.value.replace(year=today.year)
            if next_bday < today:
                next_bday = next_bday.replace(year=today.year + 1)

            days_to_bday = (next_bday - today).days
            return f"{days_to_bday} days to birthday"

    def add(rec):
        return {rec.name.value: rec}

    def delete(self):
        del self.phones

    def edit(self, phone):
        self.phones[0].value = phone


# Test
if __name__ == '__main__':
    # Add contact 1
    name = Name('Bill')
    phone = Phone()
    phone.value = "097-7777777 "
    bday = Birthday()
    bday.value = '23-01-2009'
    rec = Record(name, phone, bday)
    ab = AddressBook()
    ab.add_record(rec)

    # Add contact 2
    name = Name('Jack')
    phone = Phone()
    phone.value = "097-7777777 "
    bday = Birthday()
    bday.value = '23-01-2009'
    rec = Record(name, phone, bday)
    ab.add_record(rec)

    # Pagination
    next(ab.iterator(1))

    # Save contacts to file
    ab.save()

    # Load contacts from file
    ab = ab.load()

    # Find contact by phone
    ab.find("777")

    # Find contact by name
    ab.find("Ja")
