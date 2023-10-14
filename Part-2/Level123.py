#Level 1
#Level 2
#Level 3

class InvalidNameError(Exception):
    pass
    
class InvalidLocationError(Exception):
    pass

class InvalidRateTypeError(Exception):
    pass

class InvalidDistanceError(Exception):
    pass

class InvalidExtraServiceError(Exception):
    pass



class ExtraService:
    def __init__(self, name, price):
        self.name = name
        self.price = price



class Service:
    def __init__(self, ID, name, price):
        self.ID = ID
        self.name = name
        self.price = price

    def get_ID(self):
        return self.ID

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def set_price(self, price):
        self.price = price

    def display_info(self):
        print(f"Service - ID: {self.get_ID()}, Name: {self.get_name()}, Price: ${self.get_price()}")



class Package(Service):
    def __init__(self, ID, name, services):
        super().__init__(ID, name, 0)  # Packages have a price of 0 initially
        self.services = services

    def set_price(self):
        total_price = sum(service.get_price() for service in self.services)
        self.price = total_price * 0.8  # Price is 80% of the total price of all individual component services

    def display_info(self):
        print(f"Package - ID: {self.get_ID()}, Name: {self.get_name()}")
        print("Services included:")
        for service in self.services:
            print(f" - {service.get_name()}")

    def add_service(self, service):
        self.services.append(service)

    def remove_service(self, service):
        if service in self.services:
            self.services.remove(service)



class Customer:
    def __init__(self, ID, name):
        self.ID = ID
        self.name = name

    def get_ID(self):
        return self.ID

    def get_name(self):
        return self.name

    def get_discount(self, distance_fee):
        pass

    def display_info(self):
        pass



class BasicCustomer(Customer):
    def __init__(self, ID, name, has_previous_booking=False):
        super().__init__(ID, name)
        self.discount_rate = 0.10 if has_previous_booking else 0.0

    def get_discount_rate(self):
        return self.discount_rate

    def set_discount_rate(self, rate):
        self.discount_rate = rate

    def get_discount(self, distance_fee):
        return self.discount_rate * distance_fee

    def display_info(self):
        print(f"Basic Customer - ID: {self.get_ID()}, Name: {self.get_name()}, Discount Rate: {self.discount_rate * 100}%")



class EnterpriseCustomer(Customer):
    def __init__(self, ID, name, discount_rate1=0.15, discount_rate2=0.20, threshold=100):
        super().__init__(ID, name)
        self.discount_rate1 = discount_rate1
        self.discount_rate2 = discount_rate2
        self.threshold = threshold

    def get_discount(self, distance_fee):
        if distance_fee < self.threshold:
            return self.discount_rate1 * distance_fee
        else:
            return self.discount_rate2 * distance_fee

    def display_info(self):
        print(f"Enterprise Customer - ID: {self.get_ID()}, Name: {self.get_name()}")
        print(f"Discount Rate (Threshold < {self.threshold}): {self.discount_rate1 * 100}%")
        print(f"Discount Rate (Threshold >= {self.threshold}): {self.discount_rate2 * 100}%")

    def set_discount_rates(self, rate1, rate2):
        self.discount_rate1 = rate1
        self.discount_rate2 = rate2

    def set_threshold(self, threshold):
        self.threshold = threshold




class Location:
    def __init__(self, ID, name):
        self.ID = ID
        self.name = name

    def get_ID(self):
        return self.ID

    def get_name(self):
        return self.name

    def display_info(self):
        print(f"Location - ID: {self.get_ID()}, Name: {self.get_name()}")



class Rate:
    def __init__(self, ID, name, price_per_km):
        self.ID = ID
        self.name = name
        self.price_per_km = price_per_km

    def get_ID(self):
        return self.ID

    def get_name(self):
        return self.name

    def get_price_per_km(self):
        return self.price_per_km

    def display_info(self):
        print(f"Rate - ID: {self.get_ID()}, Name: {self.get_name()}, Price per km: ${self.get_price_per_km()}")

class Booking:
    def __init__(self, customer, rate):
        self.trip = Trip(customer, rate)

    def add_destination(self, location, distance):
        self.trip.add_destination(location, distance)

    def set_extra_service(self, extra_service):
        self.trip.set_extra_service(extra_service)

    def compute_cost(self):
        return self.trip.compute_cost()



class ExtraServiceManager:
    def __init__(self):
        self.services = []

    def add_service(self, service):
        self.services.append(service)

    def list_services(self):
        print("\nExisting Extra Services/Packages:")
        for i, service in enumerate(self.services, start=1):
            print(f"{i}. Service: {service.name}, Price: ${service.price}")



class Records:
    def __init__(self):
        self.customers = []
        self.locations = []
        self.rates = []
        self.services = []

    def read_customers(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                customer_id = data[0].strip()  
                customer_name = data[1].strip()  
                customer_type = data[2].strip()  

                if customer_type == 'B':
                    discount_rate = float(data[3]) if len(data) > 3 else 0.10  
                    customer = BasicCustomer(customer_id, customer_name, has_previous_booking=True)
                    customer.set_discount_rate(discount_rate)
                elif customer_type == 'E':
                    discount_rate = float(data[3]) if len(data) > 3 else 0.15 
                    threshold = int(data[4]) if len(data) > 4 else 100  
                    customer = EnterpriseCustomer(customer_id, customer_name, discount_rate1=discount_rate, discount_rate2=discount_rate + 0.05, threshold=threshold)
                else:
                    print(f"Invalid customer type: {customer_type}")
                    continue
                
                self.customers.append(customer)

    def read_locations(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                location_id = data[0].strip()
                location_name = data[1].strip()  # Fix: Properly extract the location name
                location = Location(location_id, location_name)
                self.locations.append(location)

    def read_rates(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                rate_id, rate_name, price_per_km = data[0], data[1], float(data[2])
                rate = Rate(rate_id, rate_name, price_per_km)
                self.rates.append(rate)

    def read_services(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                data = line.strip().split(', ')
                id_, name = data[0], data[1]
                if id_.startswith('S'):
                    price = float(data[2])
                    service = Service(id_, name, price)
                elif id_.startswith('P'):
                    service_ids = data[2:]
                    component_services = [s for s in self.services if s.get_ID() in service_ids]
                    package = Package(id_, name, component_services)
                    package.set_price()
                    service = package
                else:
                    print(f"Invalid service/package ID: {id_}")
                    continue

                self.services.append(service)

    def find_customer(self, search_value):
        for customer in self.customers:
            if customer.get_ID() == search_value or customer.get_name() == search_value:
                return customer
        return None

    def find_location(self, search_value):
        for location in self.locations:
            if location.get_ID() == search_value or location.get_name() == search_value:
                return location
        return None

    def find_location_by_name(self, name):
        for location in self.locations:
            if location.get_name() == name:
                return location
        return None


    def find_rate(self, search_value):
        for rate in self.rates:
            if rate.get_ID() == search_value or rate.get_name() == search_value:
                return rate
        return None

    def find_service(self, search_value):
        for service in self.services:
            if service.get_ID() == search_value or service.get_name() == search_value:
                return service
        return None

    def list_customers(self):
        for customer in self.customers:
            print(f"Customer ID: {customer.get_ID()}, Name: {customer.get_name()}")
            if isinstance(customer, BasicCustomer):
                print(f"Type: Basic Customer, Discount Rate: {customer.get_discount_rate() * 100}%")
            elif isinstance(customer, EnterpriseCustomer):
                print(f"Type: Enterprise Customer, Rate 1: {customer.discount_rate1 * 100}%, Rate 2: {customer.discount_rate2 * 100}%, Threshold: ${customer.threshold}")

    def list_locations(self):
        for location in self.locations:
            print(f"Location ID: {location.get_ID()}, Name: {location.get_name()}")

    def list_rates(self):
        for rate in self.rates:
            print(f"Rate ID: {rate.get_ID()}, Name: {rate.get_name()}, Price per km: ${rate.get_price_per_km()}")

    def list_services(self):
        for service in self.services:
            service.display_info()

    def add_location(self, ID, name):
        location = Location(ID, name)
        self.locations.append(location)

    def add_customer(self, ID, name, customer_type):
        if customer_type == 'B':
            customer = BasicCustomer(ID, name)
        elif customer_type == 'E':
            customer = EnterpriseCustomer(ID, name)
        else:
            raise ValueError("Invalid customer type. Use 'B' for Basic or 'E' for Enterprise.")

        self.customers.append(customer)

    def adjust_basic_customer_discount(self, new_discount_rate):
        try:
            new_discount_rate = float(new_discount_rate)
            if new_discount_rate <= 0:
                raise ValueError("Discount rate must be a positive number.")
        except ValueError:
            raise ValueError("Invalid discount rate. Please enter a valid positive number.")

        for customer in self.customers:
            if isinstance(customer, BasicCustomer):
                customer.set_discount_rate(new_discount_rate)

    def adjust_enterprise_customer_discount(self, customer_name_or_id, new_discount_rate):
        customer = self.find_customer(customer_name_or_id)
        if customer is None or not isinstance(customer, EnterpriseCustomer):
            raise InvalidCustomerError("Invalid Enterprise customer.")
        customer.set_discount_rate1(new_discount_rate)



class Service:
    def __init__(self, ID, name, price):
        self.ID = ID
        self.name = name
        self.price = price

    def get_ID(self):
        return self.ID

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def set_price(self, price):
        self.price = price

    def display_info(self):
        print(f"Service - ID: {self.get_ID()}, Name: {self.get_name()}, Price: ${self.get_price()}")


class Package(Service):
    def __init__(self, ID, name, services):
        super().__init__(ID, name, 0) 
        self.services = services

    def set_price(self):
        total_price = sum(service.get_price() for service in self.services)
        self.price = total_price * 0.8  

    def display_info(self):
        print(f"Package - ID: {self.get_ID()}, Name: {self.get_name()}")
        print("Services included:")
        for service in self.services:
            print(f" - {service.get_name()}")

    def add_service(self, service):
        self.services.append(service)

    def remove_service(self, service):
        if service in self.services:
            self.services.remove(service)



class Trip:
    def __init__(self, customer, rate):
        self.customer = customer
        self.rate = rate
        self.destinations = []
        self.distance = 0
        self.extra_service = None

    def add_destination(self, location, distance):
        self.destinations.append((location, distance))
        self.distance += distance

    def set_extra_service(self, extra_service):
        self.extra_service = extra_service

    def compute_cost(self):
        # Calculate cost based on destinations and distance
        basic_fee = self.rate.get_price_per_km() * self.distance
        discount = self.customer.get_discount(basic_fee)
        service_fee = self.extra_service.price if self.extra_service else 0
        total_cost = basic_fee - discount + service_fee
        return basic_fee, discount, service_fee, total_cost



class Operations:
    def __init__(self):
        self.records = Records()
        self.extra_service_manager = ExtraServiceManager()
        self.running = True

        self.extra_service_manager.add_service(ExtraService("Internet", 5))
        self.extra_service_manager.add_service(ExtraService("Snack", 3))
        self.extra_service_manager.add_service(ExtraService("Drink", 2))
        self.extra_service_manager.add_service(ExtraService("Entertainment", 7))

    def start(self):
        print("Welcome to the Taxi Booking System")
        print("Checking for data files...")

        try:
            self.records.read_customers("customers.txt")
            self.records.read_locations("locations.txt")
            self.records.read_rates("rates.txt")
            self.records.read_services("services.txt")
        except FileNotFoundError as e:
            print(f"Error: {e}")
            print("One or more data files are missing. Exiting...")
            return

        while self.running:
            self.display_menu()
            choice = input("Enter your choice (1/2/3/4/5/6/7/8/9): ")

            if choice == '1':
                self.book_trip()
            elif choice == '2':
                self.display_customers()
            elif choice == '3':
                self.display_locations()
            elif choice == '4':
                self.display_rates()
            elif choice == '5':
                self.display_services()
            elif choice == '6':
                self.exit_program()
            elif choice == '7':
                self.add_new_location()
            elif choice == '8':
                self.adjust_basic_customer_discount()
            elif choice == '9':
                self.adjust_enterprise_customer_discount()  # Add this option to call the method
            else:
                print("Invalid choice. Please enter a valid option (1/2/3/4/5/6/7/8/9).")



    def display_menu(self):
        print("\nMenu Options:")
        print("1. Book a trip")
        print("2. Display existing customers")
        print("3. Display existing locations")
        print("4. Display existing rate types")
        print("5. Display existing services/packages")
        print("6. Exit the program")
        print("7. Add a new location")
        print("8. Adjust the discount rate of Basic customers")
        print("9. Adjust the discount rate of an Enterprise customer")

    def book_trip(self):
        print("\nBooking a Trip:")

        customer_id_or_name = input("Enter customer ID or name: ")
        customer = self.records.find_customer(customer_id_or_name)
        
        if customer is None:
            print("Customer not found.")
            add_customer_option = input("Do you want to add a new customer? (y/n): ")
            
            if add_customer_option.lower() == 'y':
                self.add_new_customer()
                return  # Return to the main menu after adding the new customer
            else:
                return  # Exit booking if the customer is not found and not adding a new one


        rate_name = input("Enter rate type ID or name: ")
        rate = self.records.find_rate(rate_name)
        if rate is None:
            print("Rate type not found.")
            return

        booking = Booking(customer, rate)

        while True:
            departure = input("Enter departure location: ")
            departure_location = self.records.find_location(departure) 
            if departure_location is None :
                    print("Invalid departure location.")
                    continue
            else:
                break

        while True:   
            destination_name = input("Enter destination location ID or name: ")
            destination = self.records.find_location(destination_name)
            

            if destination is None:
                print("Invalid destination location.")
                continue

            distance = float(input("Enter distance (km): "))
            booking.add_destination(destination, distance)

            another_destination = input("Add another destination? (y/n): ")
            if another_destination.lower() != 'y':
                break

        while True:
            extra_service_choice = input("Do you want to order an extra service/package? (y/n): ")
            if extra_service_choice.lower() == 'y':
                self.order_extra_service(booking)
                break
            elif extra_service_choice.lower() == 'n':
                break
            else:
                print("Invalid choice. Please enter 'y' for yes or 'n' for no.")

        cost_result = booking.compute_cost()
        if cost_result is not None:
            basic_fee, discount, service_fee, total_cost = cost_result
            print("\n---------------------------------------------------------")
            print("Taxi Receipt")
            print("---------------------------------------------------------")
            print(f"Name: {customer.get_name()}")
            print(f"Departure: {departure}")
            print("Destinations:")
            for destination, distance in booking.trip.destinations:
                print(f" - {destination.get_name()} ({distance} km)")
            print(f"Rate: {rate.get_name()} (AUD per km)")
            print("---------------------------------------------------------")
            print(f"Basic fee: {basic_fee:.2f} (AUD)")
            print(f"Discount: {discount:.2f} (AUD)")
            print(f"Service fee: {service_fee:.2f} (AUD)")
            print("---------------------------------------------------------")
            print(f"Total cost: {total_cost:.2f} (AUD)")
        else:
            print("Booking failed due to errors in rate or customer records.")


    def display_customers(self):
        print("\nExisting Customers:")
        self.records.list_customers() 

    def display_locations(self):
        print("\nExisting Locations:")
        self.records.list_locations()

    def display_rates(self):
        print("\nExisting Rate Types:")
        self.records.list_rates()

    def display_services(self):
        print("\nExisting Services/Packages:")
        self.records.list_services()

    def add_new_location(self):
        print("\nAdding New Location:")
        location_id = input("Enter location ID: ")
        location_name = input("Enter location name: ")
        
        try:
            self.records.add_location(location_id, location_name)
            print(f"Location '{location_name}' with ID '{location_id}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")

    def order_extra_service(self, booking):
        print("\nAvailable Extra Services/Packages:")
        self.extra_service_manager.list_services()
        service_choice = input("Enter the number of the extra service/package you want to order: ")
        try:
            service_index = int(service_choice) - 1
            if 0 <= service_index < len(self.extra_service_manager.services):
                selected_service = self.extra_service_manager.services[service_index]
                booking.set_extra_service(selected_service)
                print(f"You have ordered the {selected_service.name} service for ${selected_service.price}.")
            else:
                raise InvalidExtraServiceError
        except (ValueError, InvalidExtraServiceError):
            print("Invalid choice. Please enter a valid number.")
    
    def add_new_customer(self):
        print("\nAdding New Customer:")
        customer_id = input("Enter customer ID: ")
        customer_name = input("Enter customer name: ")
        customer_type = input("Enter customer type (B for Basic, E for Enterprise): ")

        try:
            self.records.add_customer(customer_id, customer_name, customer_type)
            print(f"Customer '{customer_name}' with ID '{customer_id}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")

    def adjust_basic_customer_discount(self):
        print("\nAdjusting Discount Rate for Basic Customers:")
        new_discount_rate = input("Enter the new discount rate for Basic customers (e.g., 0.10 for 10%): ")

        try:
            new_discount_rate = float(new_discount_rate)
            if new_discount_rate <= 0:
                raise ValueError("Discount rate must be a positive number.")
        except ValueError:
            print("Invalid discount rate. Please enter a valid positive number.")
            return  # Return to the menu if the input is invalid

        self.records.adjust_basic_customer_discount(new_discount_rate)
        print(f"Discount rate for Basic customers adjusted to {new_discount_rate * 100:.2f}% successfully.")


    def adjust_enterprise_customer_discount(self):
        print("\nAdjusting Discount Rate for Enterprise Customers:")
        while True:
            customer_name_or_id = input("Enter the customer's name or ID: ")
            customer = self.records.find_customer(customer_name_or_id)

            if customer is None or not isinstance(customer, EnterpriseCustomer):
                print("Invalid Enterprise customer. Please enter a valid Enterprise customer name or ID.")
            else:
                break

        while True:
            new_discount_rate = input("Enter the new first discount rate (e.g., 0.2 for 20%): ")

            try:
                new_discount_rate = float(new_discount_rate)
                if new_discount_rate <= 0:
                    raise ValueError("Discount rate must be a positive number.")
                break
            except ValueError:
                print("Invalid input. Please enter a valid positive number for the discount rate.")

        customer.set_discount_rates(new_discount_rate, customer.discount_rate2)
        print(f"Discount rate for Enterprise customer '{customer.get_name()}' adjusted to {new_discount_rate * 100}% successfully.")

    def exit_program(self):
            self.running = False
            print("Exiting the program. Goodbye!")

if __name__ == "__main__":
    operations = Operations()
    operations.start()

