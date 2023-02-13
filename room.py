

import datetime
import doctest

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
DAYS_PER_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


class Room:
    TYPES_OF_ROOMS_AVAILABLE= ['twin', 'double', 'queen', 'king']
    
    def __init__(self, room_type, room_num, price):
        if (type(room_type), type(room_num), type(price))!=(str, int, float):
            raise AssertionError("One of the inputs is of the wrong type")
        
        if room_type.lower() not in Room.TYPES_OF_ROOMS_AVAILABLE:
            raise AssertionError("The room type is not available")
        
        if room_num<=0:
            raise AssertionError("Room number must be a positive")
        
        if price<0:
            raise AssertionError("The price cannot be negative.")
        
        self.room_type= room_type
        self.room_num= room_num
        self.price= price
        self.availability={}
                
    def __str__(self):
        return "Room "+str(self.room_num)+","+self.room_type+","+str(self.price)
    
    def set_up_room_availability(self, months_list, year):
        """
        >>> r = Room("Queen", 105, 80.0)
        >>> r.set_up_room_availability(['May', 'Jun'], 2021)
        >>> len(r.availability)
        2
        >>> len(r.availability[(2021, 6)])
        31
        >>> r.availability[(2021, 5)][5]
        True
        >>> print(r.availability[(2021, 5)][0])
        None
        
        >>> r = Room("Queen", 113, 90.0)
        >>> r.set_up_room_availability(['Feb'], 1600)
        >>> len(r.availability[(1600, 2)])
        30
        """
        DAYS_PER_MONTH_copy=[]
        for days in DAYS_PER_MONTH:
            DAYS_PER_MONTH_copy.append(days)
        
        if year/4==year//4:
            DAYS_PER_MONTH_copy[1]=29
        
        if str(year)[-2:]=="00":
            if year/400!=year//400:
                DAYS_PER_MONTH_copy[1]=28
        
        for i, month in enumerate(MONTHS):
            
            if month not in months_list:
                continue
            month_tuple= year, i+1
            self.availability[month_tuple]=[None]+[True]*DAYS_PER_MONTH_copy[i]

    def reserve_room(self, date):
        """
        >>> r = Room("Queen", 105, 80.0)
        >>> r.set_up_room_availability(['May', 'Jun'], 2021)
        >>> date1 = datetime.date(2021, 6, 20)
        >>> r.reserve_room(date1)
        >>> r.availability[(2021, 6)][20]
        False
        
        >>> r.availability[(2021, 5)][3] = False
        >>> date2 = datetime.date(2021, 5, 3)
        >>> r.reserve_room(date2)
        Traceback (most recent call last):
        AssertionError: The room is not available at the given date
        """
        dates_available= self.availability[(date.year, date.month)]
        
        if dates_available[date.day]==False:
            raise AssertionError("The room is not available at the given date")
        
        dates_available[date.day]= False

    def make_available(self, date):
        """
        >>> r = Room("Queen", 105, 80.0)
        >>> r.set_up_room_availability(['May', 'Jun'], 2021)
        >>> date1 = datetime.date(2021, 6, 20)
        >>> r.make_available(date1)
        >>> r.availability[(2021, 6)][20]
        True
        
        >>> r.availability[(2021, 5)][3] = False
        >>> date2 = datetime.date(2021, 5, 3)
        >>> r.make_available(date2)
        >>> r.availability[(2021, 5)][3]
        True
        """
        dates_available= self.availability[(date.year, date.month)]
        dates_available[date.day]= True

    def is_available(self, date1, date2):
        """
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May', 'Jun'], 2021)
        >>> date1 = datetime.date(2021, 6, 10)
        >>> date2 = datetime.date(2021, 5, 25)
        >>> r1.is_available(date1, date2)
        Traceback (most recent call last):
        AssertionError: The first date is not an earlier date than the second
        
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May', 'Jun'], 2021)
        >>> date1 = datetime.date(2021, 5, 25)
        >>> date2 = datetime.date(2021, 6, 10)
        >>> r1.is_available(date1, date2)
        True
        >>> r1.availability[(2021, 5)][28] = False
        >>> r1.is_available(date1, date2)
        False
        
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> r1.availability[(2021, 5)][3] = False
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> r1.is_available(date1, date2)
        False
        """
        if date1>=date2:
            raise AssertionError("The first date is not an earlier date than the second")
        
        date= date1
        while date<date2:
            if(date.year, date.month) not in self.availability:
                return False
            
            elif not self.availability[(date.year, date.month)][date.day]:
                return False
            
            date= date + datetime.timedelta(days=1)
        
        return True
    
    @staticmethod
    def find_available_room(rooms, room_type, date1, date2):
        """
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r2 = Room("Twin", 101, 55.0)
        >>> r3 = Room("Queen", 107, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> r2.set_up_room_availability(['May'], 2021)
        >>> r3.set_up_room_availability(['May'], 2021)
        >>> r1.availability[(2021, 5)][8] = False
        >>> r = [r1, r2, r3]
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> my_room = Room.find_available_room(r, 'Queen', date1, date2)
        >>> my_room == r3
        True
        >>> r3.availability[(2021, 5)][3] = False
        >>> my_room = Room.find_available_room(r, 'Queen', date1, date2)
        >>> print(my_room)
        None
        
        >>> r = Room("King", 110, 120.0)
        >>> r.set_up_room_availability(['Dec'], 2021)
        >>> r.set_up_room_availability(['Jan'], 2022)
        >>> date1 = datetime.date(2021, 12, 20)
        >>> date2 = datetime.date(2022, 1, 8)
        >>> my_room = Room.find_available_room([r], 'Queen', date1, date2)
        >>> print(my_room)
        None
        >>> my_room = Room.find_available_room([r], 'King', date1, date2)
        >>> my_room == r
        True
        """
        if date1>date2:
            raise AssertionError("The first date is not an earlier date than the second")
        
        correct_type=[]
        for room in rooms:
            if room.room_type!=room_type:
                continue
            correct_type.append(room)
        
        available_rooms=[]
        
        for room in correct_type:
            if room.is_available(date1, date2):
                available_rooms.append(room)
        
        if len(available_rooms)==0:
            return None
        
        return available_rooms[0]
