#Made By Dipesh Banerjee
#https://github.com/LostZor0
#Started on 21/08/2023
#Ended on 25/08/2023


'''
Object-oriented programming (OOP) was employed in the code to enhance the clarity, organization, 
and maintainability of the taxi booking system. By encapsulating data and behaviors within classes 
like `Customer`, `Location`, and `RateType`, OOP promotes modular design and abstraction. This 
approach facilitates code reuse, improves maintainability, and ensures data integrity. Moreover, 
OOP's support for encapsulation, inheritance, and polymorphism fosters scalability and collaboration 
among developers. Overall, OOP's structured and abstracted approach aligns well with the complexities 
of the taxi booking system, resulting in a more organized, readable, and extensible codebase. 
'''

#References
#https://www.geeksforgeeks.org/python-oops-concepts/
#https://python-textbok.readthedocs.io/en/1.0/Object_Oriented_Programming.html

#Initialize a RateType object
class RateType:
    def __init__(self, name, price_per_km):
        self.name = name
        self.price_per_km = price_per_km



#Initialize a Location object
class Location:
    def __init__(self, name):
        self.name = name
        self.distance = 0.0



#Initialize a Customer object
class Customer:
    def __init__(self, name):
        self.name = name
        self.existing = False
        self.total_spent = 0.0
        self.bookings = []

    #Set the customer as an existing customer
    def set_existing(self):
        self.existing = True

    #Check if the customer has an existing discount
    def has_existing_discount(self):
        return self.existing

    #Add the given amount to the total spent by the customer    
    def add_spent_amount(self, amount):
        self.total_spent += amount

    #Get the total amount spent by the customer  
    def get_total_spent(self):
        return self.total_spent

    #Add a booking to the customer's booking history     
    def add_booking(self, booking):
        self.bookings.append(booking)



#Initialize a TaxiBooking object
class TaxiBooking:
    def __init__(self):
        self.customers = []
        self.locations = []
        self.rate_types = []
        self.initialize_data()

    #Saves the pre-given data from the questions
    def initialize_data(self):
        self.locations = [Location("Melbourne"), Location("Chadstone"), Location("Clayton"), Location("Brighton"), Location("Fitzroy")]
        self.rate_types = [RateType("standard", 1.5), RateType("peak", 1.8), RateType("weekends", 2), RateType("holiday", 2.5)]
        self.customers = [Customer("Louis"), Customer("Ella")]
        for customer in self.customers:
            customer.set_existing()

    def display_message(self, message):
        print(message)

    #Gets the customer name  
    def get_customer_name(self):
        while True:
            name = input("Enter the customer's name: ")
            if name.isalpha():
                return name
            else:
                print("Invalid name. Names must contain only alphabet characters.\n")
   
    #Gets the Location 
    def get_location(self, message):
        self.display_message(message)
        while True:
            for idx, location in enumerate(self.locations, start=1):
                print(f"{idx}. {location.name}")
            choice = input("Enter the location number: ")
            if choice.isdigit() and 1 <= int(choice) <= len(self.locations):
                chosen_location = self.locations[int(choice) - 1]
                if message.startswith("Enter the destination"):
                    departure_location = self.departure.name if hasattr(self, "departure") else None
                    if departure_location != chosen_location.name:
                        return chosen_location
                    else:
                        print("Invalid destination. Destination must be different from departure.\n")
                else:
                    return chosen_location
            else:
                print("Invalid choice. Please enter a valid location number.\n")

    #Gets the rate type
    def get_rate_type(self):
        self.display_message("Select a rate type:")
        while True:
            for idx, rate_type in enumerate(self.rate_types, start=1):
                print(f"{idx}. {rate_type.name}")
            choice = input("Enter the rate type number: ")
            if choice.isdigit() and 1 <= int(choice) <= len(self.rate_types):
                return self.rate_types[int(choice) - 1]
            else:
                print("Invalid choice. Please enter a valid rate type number.")

    #Gets the distance
    def get_distance(self):
        while True:
            try:
                distance = float(input("Enter the distance (in km): "))
                if distance <= 0:
                    print("Distance must be a positive number.\n")
                else:
                    return distance
            except ValueError:
                print("Invalid distance. Please enter a valid number.\n")

    #Calculates the distance fee
    def calculate_distance_fee(self, distance, rate_type):
        return distance * rate_type.price_per_km

    #Books a taxi trip for a customer
    def book_taxi(self):
        name = self.get_customer_name()
        customer = None
        for existing_customer in self.customers:
            if existing_customer.name == name:
                customer = existing_customer
                break
        if customer is None:
            customer = Customer(name)
            self.customers.append(customer)

        departure = self.get_location("Enter the departure location:")
        self.departure = departure

        destinations = []
        while True:
            destination = self.get_location("Enter the destination location (enter n to finish):")
            if destination.name == departure.name:
                print("Invalid destination. Destination must be different from departure.\n")
            elif destination in destinations:
                print("Invalid destination. Destination must be different from previous destinations.\n")
            else:
                distance = self.get_distance()
                destination.distance = distance
                destinations.append(destination)

            another_destination = input("Add another destination? (y/n): ").lower()
            if another_destination == "n":
                break
            elif another_destination != "y":
                print("Invalid input. Please enter 'y' or 'n'.\n")

        total_distance = sum([destination.distance for destination in destinations])
        rate_type = self.get_rate_type()

        distance_fee = self.calculate_distance_fee(total_distance, rate_type)
        basic_fee = 4.2
        discount = 0
        if customer.has_existing_discount():
            discount = 0.1 * distance_fee
        total_cost = distance_fee + basic_fee - discount
        self.display_receipt(customer, departure, destinations, total_distance, rate_type, basic_fee, distance_fee, discount, total_cost)

        # Update customer's spent amount and booking history
        customer.add_spent_amount(total_cost)
        customer.add_booking({
            "departure": departure.name,
            "destinations": [destination.name for destination in destinations],
            "total_cost": total_cost
        })

    

    def display_receipt(self, customer, departure, destinations, total_distance, rate_type, basic_fee, distance_fee, discount, total_cost):
        print("---------------------------------------------------------")
        print(" Taxi Receipt")
        print("---------------------------------------------------------")
        print(f"Name: {customer.name}")
        print(f"Departure: {departure.name}")
        for destination in destinations:
            print(f"Destination: {destination.name}")
            print(f"Distance: {destination.distance} (km)")
        print("Rate:", rate_type.price_per_km, "(AUD per km)")
        print(f"Total Distance: {total_distance} (km)")
        print("---------------------------------------------------------")
        print(f"Basic fee: {basic_fee:.2f} (AUD)")
        print(f"Distance fee: {distance_fee:.2f} (AUD)")
        print(f"Discount: {discount:.2f} (AUD)")
        print("---------------------------------------------------------")
        print(f"Total cost: {total_cost:.2f} (AUD)\n\n")

    def display_existing_customers(self):
        print("Existing Customers:")
        for customer in self.customers:
            print(customer.name)
        print('\n')

    def display_existing_locations(self):
        print("Existing Locations:")
        for location in self.locations:
            print(location.name)
        print('\n')

    def display_existing_rate_types(self):
        print("Existing Rate Types and Prices:")
        for rate_type in self.rate_types:
            print(f"{rate_type.name}: {rate_type.price_per_km:.2f}$ per km")
        print('\n')


    def add_update_rate_types(self):
        while True:
            rate_types_input = input("Enter rate types separated by commas: ").strip()
            prices_input = input("Enter corresponding prices separated by commas: ").strip()

            rate_types = [rate.strip() for rate in rate_types_input.split(',')]
            prices = [price.strip() for price in prices_input.split(',')]

            if len(rate_types) != len(prices):
                print("Number of rate types must match the number of prices.\n")
                continue
            
            valid_prices = True
            for price in prices:
                if not price.replace('.', '', 1).isdigit() or float(price) <= 0:
                    print("Invalid price. Prices must be positive numbers.\n")
                    valid_prices = False
                    break

            if valid_prices:
                for i in range(len(rate_types)):
                    rate_type_name = rate_types[i]
                    price = float(prices[i])
                    existing_rate_type = None
                    for existing_rate in self.rate_types:
                        if existing_rate.name == rate_type_name:
                            existing_rate.price_per_km = price
                            existing_rate_type = existing_rate
                            break
                    if existing_rate_type is None:
                        new_rate_type = RateType(rate_type_name, price)
                        self.rate_types.append(new_rate_type)
                break

    def add_new_locations(self):
        locations_input = input("Enter new locations separated by commas: ").strip()
        new_locations = [location.strip() for location in locations_input.split(',')]
        
        for new_location in new_locations:
            if any(new_location == loc.name for loc in self.locations):
                print(f"{new_location} is an existing location and will not be added.")
            else:
                self.locations.append(Location(new_location))
                print(f"{new_location} has been added as a new location.")

    def display_most_valuable_customer(self):
        most_valuable_customer = max(self.customers, key=lambda customer: customer.get_total_spent())
        print(f"Most valuable customer: {most_valuable_customer.name}")
        print(f"Total money spent: {most_valuable_customer.get_total_spent():.2f} AUD")
        print('\n')

    def display_customer_booking_history(self):
        customer_name = input("Enter the name of the customer: ")
        found_customer = False
        for customer in self.customers:
            if customer.name == customer_name:
                found_customer = True
                print(f"This is the booking history of {customer_name}:")
                print("Booking".ljust(10), "Departure".ljust(20), "Destination".ljust(30), "Total cost".ljust(10))
                for idx, booking in enumerate(customer.bookings, start=1):
                    print(f"{idx}".ljust(10), f"{booking['departure']}".ljust(20), f"{', '.join(booking['destinations'])}".ljust(30), f"{booking['total_cost']:.2f}".ljust(10))
                print('\n')    
                break
        if not found_customer:
            print("Customer not found. Please enter a valid customer name.")

    def run(self):
        while True:
            print('\n')
            print("Welcome to the taxi management system:")
            print("\n#####################################################################################")
            print("Menu:")
            print("1. Book a Trip")
            print("2. Add/Update Rate Types and Prices")
            print("3. Display Existing Customers")
            print("4. Display Existing Locations")
            print("5. Display Existing Rate Types")
            print("6. Add New Locations")
            print("7. Display Most Valuable Customer")
            print("8. Display Customer Booking History")
            print("0. Exit")
            print("#####################################################################################")

            choice = input("Enter your choice: ")
            if choice == "1":
                self.book_taxi()
            elif choice == "2":
                self.add_update_rate_types()
            elif choice == "3":
                self.display_existing_customers()
            elif choice == "4":
                self.display_existing_locations()
            elif choice == "5":
                self.display_existing_rate_types()
            elif choice == "6":
                self.add_new_locations()
            elif choice == "7":
                self.display_most_valuable_customer()
            elif choice == "8":
                self.display_customer_booking_history()
            elif choice == "0":
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please enter a valid option.")

# Main program
if __name__ == "__main__":
    taxi_booking = TaxiBooking()
    taxi_booking.run()
