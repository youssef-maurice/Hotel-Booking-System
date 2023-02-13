
import datetime
import random
from room import Room, MONTHS, DAYS_PER_MONTH
import doctest

class Reservation:
    booking_numbers=[]
    
    def __init__(self, name, room_reserved, date1, date2, booking_number=None):
        """
        >>> random.seed(987)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> my_reservation = Reservation('Mrs. Santos', r1, date1, date2)
        >>> print(my_reservation.check_in)
        2021-05-03
        >>> print(my_reservation.check_out)
        2021-05-10
        >>> my_reservation.booking_number
        1953400675629
        >>> r1.availability[(2021, 5)][9]
        False
        >>> r1.availability[(2021, 5)][10]
        True
        """
        if not room_reserved.is_available(date1, date2):
            raise AssertionError("The room is not available at the specified dates")
        
        self.name= name
        self.room_reserved= room_reserved
        self.check_in= date1
        self.check_out= date2
        self.booking_number= booking_number
        
        if self.booking_number== None:
            self.booking_number= random.randint(1000000000000, 9999999999999)
            
            while self.booking_number in Reservation.booking_numbers:
                self.booking_number= random.randint(1000000000000, 9999999999999)
            
            Reservation.booking_numbers.append(self.booking_number)
        
        else:
            if type(self.booking_number)!=int:
                raise AssertionError("The booking number must be a digit")
            
            if len(str(self.booking_number))!=13:
                raise AssertionError("The booking number must be 13 digits long")
            
            if self.booking_number in Reservation.booking_numbers:
                raise AssertionError("The booking number is currently unavailable")
        
        for day in range((date2-date1).days):
            room_reserved.reserve_room(date1+datetime.timedelta(day))
        
    def __str__(self):
        """
        >>> random.seed(987)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> my_reservation = Reservation('Mrs. Santos', r1, date1, date2)
        >>> print(my_reservation)
        Booking number: 1953400675629
        Name: Mrs. Santos
        Room reserved: Room 105,Queen,80.0
        Check-in date: 2021-05-03
        Check-out date: 2021-05-10
        """
        line1= "Booking number: "+str(self.booking_number)
        line2= "Name: "+self.name
        line3= "Room reserved: "+str(self.room_reserved)
        line4= "Check-in date: "+str(self.check_in)
        line5= "Check-out date: "+str(self.check_out)
        
        return line1+"\n"+line2+"\n"+line3+"\n"+line4+"\n"+line5

    def to_short_string(self):
        """
        >>> random.seed(987)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> my_reservation = Reservation('Mrs. Santos', r1, date1, date2)
        >>> my_reservation.to_short_string()
        '1953400675629--Mrs. Santos'
        """
        return str(self.booking_number)+"--"+self.name

    @classmethod
    def from_short_string(cls, string, date1, date2, room_reserved):
        """
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 4)
        >>> my_reservation = Reservation.from_short_string('1953400675629--Mrs. Santos', date1, date2, r1)
        >>> print(my_reservation.check_in)
        2021-05-03
        >>> print(my_reservation.check_out)
        2021-05-04
        >>> my_reservation.booking_number
        1953400675629
        >>> r1.availability[(2021, 5)][3]
        False
        """
        name_and_number= string.split("--")
        name= name_and_number[1]
        booking_number=int(name_and_number[0])
        
        return cls(name, room_reserved, date1, date2, booking_number)

    @staticmethod
    def get_reservations_from_row(room_obj, list_tups):
        """
        >>> random.seed(987)
        >>> Reservation.booking_numbers = [] # needs to be reset for the test below to pass
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(MONTHS, 2021)
        >>> rsv_strs =  [(2021, 'May', 3, '1953400675629--Jack'), (2021, 'May', 4, '1953400675629--Jack')]
        >>> rsv_dict = Reservation.get_reservations_from_row(r1, rsv_strs)
        >>> print(rsv_dict[1953400675629])
        Booking number: 1953400675629
        Name: Jack
        Room reserved: Room 105,Queen,80.0
        Check-in date: 2021-05-03
        Check-out date: 2021-05-05
        """
        new_list=[] 
        my_dict={}
        new_dict={}
        
        for tup in list_tups:
            
            if len(tup[3])!=0:
                year, month, day, short_string= tup
                short_list= short_string.split("--")
                booking_num, name= short_list
                new_list.append((year ,month, day, booking_num, name))
        
        for tup in new_list:
            
            if tup[3] in my_dict:
                my_dict[tup[3]].append(tup)
            
            else:
                my_dict[tup[3]]=[tup]
        list_dates=[]
        
        for key, value in my_dict.items():
            list_dates=[]
            
            for tup in value:
                year, month, day, booking_num, name= tup
                short_string= str(booking_num)+"--"+name
                int_month= MONTHS.index(month)+1
                date= datetime.date(tup[0], int_month, tup[2])
                list_dates.append(date)
            
            check_in= min(list_dates)
            check_out= max(list_dates)+ datetime.timedelta(days=1)
            new_dict[int(key)]= Reservation.from_short_string(short_string, check_in, check_out, room_obj)
        
        return new_dict
