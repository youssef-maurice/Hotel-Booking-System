
import datetime
import random
from hotel import Hotel
import matplotlib
import os
import doctest
from reservation import Reservation

class Booking:
    
    def __init__(self, hotels):
        self.hotels= hotels
        
    @classmethod
    def load_system(cls):
        """
        >>> system = Booking.load_system()
        >>> len(system.hotels)
        2
        >>> system.hotels[1].name
        'The Great Northern Hotel'
        >>> print(system.hotels[1].rooms[314])
        Room 315,Queen,129.99
        """
        hotels=[]
        list_hotels= os.listdir('hotels')
        
        for file in list_hotels:
            hotel= Hotel.load_hotel(file)
            hotels.append(hotel)
        
        return cls(hotels)
        
    def menu(self):
        """
        >>> booking = Booking.load_system()
        >>> booking.menu()
        Welcome to Booking System
        What would you like to do?
        1 Make a reservation
        2 Cancel a reservation
        3 Look up a reservation
        """
        
        print("Welcome to Booking System")
        print("What would you like to do?")
        options= {1: "Make a reservation", 2: "Cancel a reservation", 3: "Look up a reservation"}
        
        for option in options:
            print(option, options[option])
        
        choice= input()
        
        if int(choice)==1:
            self.create_reservation()
        
        elif int(choice)==2:
            self.cancel_reservation()
        
        elif int(choice)==3:
            self.lookup_reservation()
        
        elif choice=="xyzzy":
            self.delete_reservations_at_random()
        
        for hotel_obj in self.hotels:
            hotel_obj.save_hotel()
        
    def create_reservation(self):
        user_name= input("Please enter your name: ")
        print("Hi "+ user_name +"! Which hotel would you like to book?")
        
        for i, hotel_obj in enumerate(self.hotels):
            print(i+1, str(hotel_obj.name))
        
        hotel_num= int(input())
        print("which type o froom would you like?")
        room_types= self.hotels[hotel_num-1].get_available_room_types()
        
        for i, room_type in enumerate(room_types):
            print(i+1, room_type)
        
        room_type_num= int(input())
        
        check_in_date= input("Enter check-in date (YYYY-MM-DD): ")
        check_in_date= check_in_date.split("-")
        check_in_year, check_in_month, check_in_day= check_in_date[0], check_in_date[1], check_in_date[2]
        date1= datetime.date(int(check_in_year), int(check_in_month), int(check_in_day))
        
        check_out_date= input("Enter check-out date (YYYY-MM-DD): ")
        check_out_date= check_out_date.split("-")
        check_out_year, check_out_month, check_out_day= check_out_date[0], check_out_date[1], check_out_date[2]
        date2= datetime.date(int(check_out_year), int(check_out_month), int(check_out_day))
        
        print("Ok. Making your reservation for a "+ room_types[room_type_num-1] +" room.")
        
        booking_num= self.hotels[hotel_num-1].make_reservation(user_name, room_types[room_type_num-1], date1, date2)
        print("Your reservation number is: ", booking_num )
        
        receipt= str(round(self.hotels[hotel_num-1].get_receipt([booking_num]), 2))
        print("Your total amount due is: $"+ receipt)
        print("Thank you!")
        
    def cancel_reservation(self):
        user_num= int(input("Please enter your booking number: "))
        
        for hotel_obj in self.hotels:
            booking_nums=[]
            
            for reservation in hotel_obj.reservations:
                booking_nums.append(reservation)
            
            hotel_obj.cancel_reservation(user_num)
            
            if len(booking_nums)== len(hotel_obj.reservations):
                print("Could not find a reservation with that booking number.")
            
            else:
                print("Cancelled successfully.")
    
    def lookup_reservation(self):
        user_answer= input("Do you have your booking number(s)? ")
        
        if user_answer.lower()=="yes":
            booking_nums=[]
            user_num= input("Please enter a booking number (or 'end'): ")
            
            if user_num!='end':
                booking_nums.append(int(user_num))
            
            while user_num!= 'end':
                user_num= input("Please enter a booking number (or 'end'): ")
                
                if user_num!='end':
                    booking_nums.append(int(user_num))
            
            for hotel_obj in self.hotels:
                
                for booking_num in booking_nums:
                    print('Reservation found at '+str(hotel_obj.name)+':')
                    
                    try:
                        print(hotel_obj.reservations[booking_num])
                        print("Total amount due: $"+str(round(hotel_obj.get_receipt([booking_num]), 2)))
                    
                    except:
                        print("No reservation was found with the number: " +str(booking_num))
        
        else:
            user_name= input("Please enter your name: ")
            chosen_hotel= input("Please enter the hotel you are booked at: ")
            room_num= input("Enter the reserved room number: ")
            check_in= input("Enter the check-in date (YYYY-MM-DD): ")
            check_out= input("Enter the check-out date (YYYY-MM-DD): ")
            
            for hotel_obj in self.hotels:
                
                if hotel_obj.name== chosen_hotel:
                    message=[]
                    
                    for booking_num, reservation in hotel_obj.reservations.items():
                        condition1= reservation.room_reserved.room_num== int(room_num)
                        condition2= reservation.name.lower()== user_name.lower()
                        condition3= str(reservation.check_in)== check_in
                        condition4= str(reservation.check_out)== check_out
                        
                        if condition1 and condition2 and condition3 and condition4:
                            print("Reservation found under booking number "+str(booking_num)+'.')
                            print("Here are the details: ")
                            print(reservation)
                            print("Total amount due: $"+str(round(hotel_obj.get_receipt([booking_num]), 2)))
                            message.append("a room was found.")
                        
                        if len(message)==0:
                            print("No room was found under this information.")
        
    def delete_reservations_at_random(self):
        """
        >>> random.seed(1338)
        >>> booking = Booking.load_system()
        >>> booking.delete_reservations_at_random()
        You said the magic word!
        >>> len(booking.hotels[1].reservations)
        0
        >>> len(booking.hotels[0].reservations)
        1
        """
        print("You said the magic word!")
        hotel_to_delete= random.randint(0, len(self.hotels)-1)
        booking_nums=[]
        
        for reservation in self.hotels[hotel_to_delete].reservations:
            booking_nums.append(reservation)
        
        for reservation in booking_nums:
            self.hotels[hotel_to_delete].cancel_reservation(reservation)
