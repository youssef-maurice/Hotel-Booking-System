
import datetime
import random
import copy
import os
from room import Room, MONTHS, DAYS_PER_MONTH
from reservation import Reservation
import doctest

class Hotel:
    def __init__(self, name, rooms=[], reservations={}):
        self.name= name
        self.rooms= copy.deepcopy(rooms)
        self.reservations= copy.deepcopy(reservations)
        
    def make_reservation(self, name, type_of_room, check_in, check_out):
        """
        >>> random.seed(987)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> h = Hotel("Secret Nugget Hotel", [r1])
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> h.make_reservation("Mrs. Santos", "Queen", date1, date2)
        1953400675629
        >>> print(h.reservations[1953400675629])
        Booking number: 1953400675629
        Name: Mrs. Santos
        Room reserved: Room 105,Queen,80.0
        Check-in date: 2021-05-03
        Check-out date: 2021-05-10
        """
        available_room= Room.find_available_room(self.rooms, type_of_room, check_in, check_out)
        
        if available_room==None:
            raise AssertionError("No rooms of this type are available")
        
        booked_room= Reservation(name, available_room, check_in, check_out)
        self.reservations[booked_room.booking_number]= booked_room
        
        return booked_room.booking_number
        
    def get_receipt(self, booking_nums):
        """
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r2 = Room("Twin", 101, 55.0)
        >>> r3 = Room("Queen", 107, 80.0)
        >>> r1.set_up_room_availability(['May', 'Jun'], 2021)
        >>> r2.set_up_room_availability(['May', 'Jun'], 2021)
        >>> r3.set_up_room_availability(['May', 'Jun'], 2021)
        >>> h = Hotel("Secret Nugget Hotel", [r1, r2, r3])
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> num1 = h.make_reservation("Mrs. Santos", "Queen", date1, date2)
        >>> h.get_receipt([num1])
        560.0
        
        >>> date3 = datetime.date(2021, 6, 5)
        >>> num2 = h.make_reservation("Mrs. Santos", "Twin", date1, date3)
        >>> h.get_receipt([num1, num2])
        2375.0
        
        >>> h.get_receipt([123])
        0.0
        """
        total=0.0
        
        for booking_num in booking_nums:
            
            if booking_num not in self.reservations:
                continue
            
            date1= self.reservations[booking_num].check_in
            date2= self.reservations[booking_num].check_out
            days_stayed= (date2-date1).days
            price_for_room= days_stayed*self.reservations[booking_num].room_reserved.price
            
            total+=price_for_room
        
        return total
    
    def get_reservation_for_booking_number(self, booking_num):
        """
        >>> random.seed(137)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> h = Hotel("Secret Nugget Hotel", [r1])
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> num1 = h.make_reservation("Mrs. Santos", "Queen", date1, date2)
        >>> rsv = h.get_reservation_for_booking_number(num1)
        >>> print(rsv)
        Booking number: 4191471513010
        Name: Mrs. Santos
        Room reserved: Room 105,Queen,80.0
        Check-in date: 2021-05-03
        Check-out date: 2021-05-10
        """
        return self.reservations[booking_num]
    
    def cancel_reservation(self, booking_num):
        """
        >>> random.seed(137)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> h = Hotel("Hotel California", [r1])
        >>> r1.availability[(2021, 5)][5]
        True
        >>> h.rooms[0].availability[(2021, 5)][5]
        True
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> num1 = h.make_reservation("Mrs. Los Santos", "Queen", date1, date2)
        >>> r1.availability[(2021, 5)][5]
        True
        >>> h.rooms[0].availability[(2021, 5)][5]
        False
        >>> h.cancel_reservation(num1)
        >>> r1.availability[(2021, 5)][5]
        True
        >>> h.rooms[0].availability[(2021, 5)][5]
        True
        """
        try:
            date1= self.reservations[booking_num].check_in
        
        except KeyError:
            return
        
        date2= self.reservations[booking_num].check_out
        days_stayed= (date2-date1).days
        
        for day in range(days_stayed):
            date= date1+datetime.timedelta(day)
            self.reservations[booking_num].room_reserved.make_available(date)
        
        del self.reservations[booking_num]
        
    def get_available_room_types(self):
        """
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r2 = Room("Twin", 101, 55.0)
        >>> r3 = Room("Queen", 107, 80.0)
        >>> r1.set_up_room_availability(['May', 'Jun'], 2021)
        >>> r2.set_up_room_availability(['May', 'Jun'], 2021)
        >>> r3.set_up_room_availability(['May', 'Jun'], 2021)
        >>> h = Hotel("Secret Nugget Hotel", [r1, r2, r3])
        >>> types = h.get_available_room_types()
        >>> types.sort()
        >>> types
        ['Queen', 'Twin']
        """
        room_types=[]
        for room in self.rooms:
            
            if room.room_type in room_types:
                continue
            
            room_types.append(room.room_type)
        
        return room_types
    
    @staticmethod
    def load_hotel_info_file(filename):
        """
        >>> hotel_name, rooms = Hotel.load_hotel_info_file('hotels/overlook_hotel/hotel_info.txt')
        >>> hotel_name
        'Overlook Hotel'
        >>> print(len(rooms))
        500
        >>> print(rooms[236])
        Room 237,Twin,99.99
        """
        fobj = open(filename, 'r')
        file_content = fobj.read()
        
        list_of_contents= file_content.split('\n')[:-1]
        hotel_name= list_of_contents[0]
        rooms_in_file= list_of_contents[1:]
        rooms=[]
        
        for room in rooms_in_file:
            room= room.split(',')
            room_num= int(room[0].split()[1])
            room_type=str(room[1])
            price= float(room[2])
            room= Room(room_type, room_num, price)
            rooms.append(room)
        
        fobj.close()
        
        return hotel_name, rooms
    
    def save_hotel_info_file(self):
        """
        >>> r1 = Room("Double", 101, 99.99)
        >>> r1.set_up_room_availability(['Oct', 'Nov', 'Dec'], 2021)
        >>> h = Hotel("Queen Elizabeth Hotel", [r1], {})
        >>> h.save_hotel_info_file()
        >>> fobj = open('hotels/queen_elizabeth_hotel/hotel_info.txt', 'r')
        >>> fobj.read()
        'Queen Elizabeth Hotel\\nRoom 101,Double,99.99\\n'
        >>> fobj.close()
        """
        folder= self.name.lower()
        folder= folder.replace(" ", "_")
        filename= "hotel_info.txt"
        fobj= open('hotels/'+folder+"/"+filename, 'w', encoding = 'utf-8')
        
        for room in self.rooms:  
            fobj.write(self.name+'\n'+str(room)+'\n')
        
        fobj.close()
    
    @staticmethod
    def load_reservation_strings_for_month(folder, month, year):
        final_dict= {}
        filename= str(year)+"_"+month+".csv"
        fobj = open('hotels/'+folder+"/"+filename, 'r')
        day_in_month=1
        
        for row in fobj:
            list_of_days=[]
            row= row.strip('\n')
            row_content= row.split(",")
            room_num= int(row_content[0])
            
            for day in row_content:
                
                if day== str(room_num):
                    continue
                
                if day=="":
                    list_of_days.append((year, month, row_content.index(day), ""))
                    row_content.insert(row_content.index(day), None)
                    row_content.remove(day)
                
                else:
                    list_of_days.append((year, month, row_content.index(day), day))
                    row_content.insert(row_content.index(day), None)
                    row_content.remove(day)
            
            final_dict[room_num]= list_of_days
        
        return final_dict

    def save_reservations_for_month(self, month, year):
        """
        >>> random.seed(987)
        >>> r1 = Room("Double", 237, 99.99)
        >>> r1.set_up_room_availability(['Oct', 'Nov', 'Dec'], 2021)
        >>> Reservation.booking_numbers = []
        >>> h = Hotel("Queen Elizabeth Hotel", [r1], {})
        >>> date1 = datetime.date(2021, 10, 30)
        >>> date2 = datetime.date(2021, 12, 23)
        >>> num = h.make_reservation("Jack", "Double", date1, date2)
        >>> h.save_reservations_for_month('Oct', 2021)
        >>> fobj = open('hotels/queen_elizabeth_hotel/2021_Oct.csv', 'r')
        >>> fobj.read()
        '237,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,1953400675629--Jack,1953400675629--Jack\\n'
        >>> fobj.close()
        """
        folder= self.name.lower()
        folder= folder.replace(" ", "_")
        filename= str(year)+'_'+month+'.csv'
        fobj= open('hotels/'+folder+"/"+filename, 'w', encoding = 'utf-8')
        
        for booking_num in self.reservations:
            nights_in_month= self.reservations[booking_num].room_reserved.availability[(year, MONTHS.index(month)+1)]
            nights_in_month_copy= copy.deepcopy(nights_in_month)
            name= self.reservations[booking_num].to_short_string()
            num=self.reservations[booking_num].room_reserved.room_num
            str_to_write=str(num)+','
        
        for night in nights_in_month:
            
            if night== None:
                continue
            
            elif night:
                str_to_write= str_to_write+','
            
            elif not night:
                
                if nights_in_month_copy.index(night)==len(nights_in_month)-1:
                    str_to_write= str_to_write+name+'\n'
                
                else:
                    str_to_write= str_to_write+name+','
                    nights_in_month_copy.remove(night)
                    nights_in_month_copy.insert(0, None)
        
        fobj.write(str_to_write)
        fobj.close()
    
    def save_hotel(self):
        """
        >>> random.seed(987)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Double", 237, 99.99)
        >>> r1.set_up_room_availability(['Oct', 'Nov', 'Dec'], 2021)
        >>> h = Hotel("Queen Elizabeth Hotel", [r1], {})
        >>> date1 = datetime.date(2021, 10, 30)
        >>> date2 = datetime.date(2021, 12, 23)
        >>> h.make_reservation("Jack", "Double", date1, date2)
        1953400675629
        >>> h.save_hotel()

        >>> fobj = open('hotels/queen_elizabeth_hotel/hotel_info.txt', 'r')
        >>> fobj.read()
        'Queen Elizabeth Hotel\\nRoom 237,Double,99.99\\n'
        >>> fobj.close()

        >>> fobj = open('hotels/queen_elizabeth_hotel/2021_Oct.csv', 'r')
        >>> fobj.read()
        '237,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,1953400675629--Jack,1953400675629--Jack\\n'
        >>> fobj.close()
        """
        hotel_filename= self.name.lower()
        hotel_filename= hotel_filename.replace(" ", "_")
        filename= 'hotels/'+ hotel_filename
        
        if not os.path.exists(filename):
            os.makedirs(filename)
        
        self.save_hotel_info_file()
        
        for room in self.rooms:
            availability= room.availability
            
            for year, month in availability:
                
                if False in availability[(year, month)]:
                    month_string= MONTHS[month-1]
                    self.save_reservations_for_month(month_string, year)
    
    @classmethod
    def load_hotel(cls, filename):
        """
        >>> random.seed(137)
        >>> Reservation.booking_numbers = []
        >>> hotel = Hotel.load_hotel('overlook_hotel')
        >>> hotel.name
        'Overlook Hotel'
        >>> str(hotel.rooms[236])
        'Room 237,Twin,99.99'
        >>> print(hotel.reservations[9998701091820])
        Booking number: 9998701091820
        Name: Jack
        Room reserved: Room 237,Twin,99.99
        Check-in date: 1975-10-30
        Check-out date: 1975-12-24
        """
        dict_room_obj={}
        rsvs={}
        room_objects= cls.load_hotel_info_file('hotels/'+filename+'/hotel_info.txt')[1]
        name= cls.load_hotel_info_file('hotels/'+filename+'/hotel_info.txt')[0]
        list_hotels= os.listdir('hotels/'+filename)
        
        for name_split in list_hotels:
            
            if 'csv' in name_split:
                name_split= name_split.split('.')
                date= name_split[0].split("_")
                year= int(date[0])
                month= date[1]
                dict_tuple= cls.load_reservation_strings_for_month(filename, month, year)
                
                for room_obj in room_objects:
                    room_obj.set_up_room_availability([month], year)
                
                if dict_room_obj!={}:
                    for room_num in dict_tuple:
                        dict_room_obj[room_num]+=dict_tuple[room_num]
                
                else:
                    dict_room_obj= dict_tuple
        
        for room_obj in room_objects:
            room_num= room_obj.room_num
            res_dict_one_room= Reservation.get_reservations_from_row(room_obj, dict_room_obj[room_num])
            
            for booking_num in res_dict_one_room:
                rsvs[booking_num]= res_dict_one_room.get(booking_num)
        
        return cls(name, room_objects, rsvs)
