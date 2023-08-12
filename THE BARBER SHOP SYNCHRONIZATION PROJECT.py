from threading import Thread, Lock, Event
import time, random, threading

customers=threading.Semaphore(0) #semaphore for synchornization
barber_sync = threading.Semaphore(0) # semaphore for synchornization
mutex = Lock() #mutex for mutual exclusion

#Interval in seconds
customerIntervalMin = 5 #Minimum time between customer arrivals
customerIntervalMax = 15 #Maximum time for customer arrival
haircutDurationMin = 10 # Minimum Duration of Haircut
haircutDurationMax = 15 # Maximum Duration Of Haircut
barber_asleep = 0 #Defines the state of barber. If barber is sleeping asleep=0 otherwise 1

class BarberShop:
	waitingCustomers = [] #Holds the names of the customers in waiting room

	def __init__(self, barber):
		self.barber = barber
		self.totalChairs = 1 #total number of seats in waiting room
		print ('Total Chairs', self.totalChairs)
		print ('Customer min interval ', customerIntervalMin)
		print ('Customer max interval ',customerIntervalMax)
		print ('Haircut min duration ' , haircutDurationMin)
		print ('Haircut max duration ', customerIntervalMax)
		print ('---------------------------------------')

	def openShop(self):
		print ('Barber shop is opening')
		workingThread = Thread(target = self.barberGoToWork)
		workingThread.start()

	def barberGoToWork(self):
		while True:
			mutex.acquire()
			#Checks for customers in waiting room
			if len(self.waitingCustomers) == 0: 
				#IF no customer barber goes to sleep
				mutex.release()
				self.barber.sleep()
			else:
				#If there are customers waiting the first arriving customer gets the hair cut
				c = self.waitingCustomers[0]
				del self.waitingCustomers[0]
				mutex.release()
				Customer.getHairCut(self, c.name)
				self.barber.cutHair(c)

	
	def enterBarberShop(self, customer):
		mutex.acquire()
		print (customer.name, 'entered the shop and is looking for a seat')
		#Checks if waiting room is full
		if len(self.waitingCustomers) >= self.totalChairs:
			# If the waiting room is full the customer balks away
			Customer.Balk(self, customer.name)
			mutex.release()
		else:
			#if the waiting room has space the arriving customer sits in the waiting chairs
			print (customer.name, 'sat down in the waiting room')
			self.waitingCustomers.append(customer)	
			global barber_asleep
			if barber_asleep:
				#Checks if barber is asleep if yes the customer wakes up the barber
				Customer.WakeBarber(customer)
			mutex.release()

class Customer:
	def __init__(self, name):
		self.name = name
	def WakeBarber(self):
		# Customer wakes up barber
		customers.release()
		global barber_asleep
		barber_asleep = 0
		print("Barber just woke up")
	def getHairCut(self, customer):
		#Customer asks for a haircut
		print(customer , "is having a haircut")
	def Balk(self, customer):
		#Customer balks away if the waiting room is full
		print("Waiting room is full.", customer, "balks away.")

class Barber:

	def sleep(self):
		#Barber goes to sleep if no more customers
		global barber_asleep
		print("Barber: Ahh, No more Customers. Let\'s get some sleep.")
		barber_asleep = 1
		customers.acquire()

	def cutHair(self, customer):
		#Set barber as busy 
		barber_sync.release()
		randomHairCuttingTime = random.randrange(haircutDurationMin, haircutDurationMax+1)
		time.sleep(randomHairCuttingTime)
		print (customer.name,' is done with his haircut.')


cust = []
cust.append(Customer('Kashif'))
cust.append(Customer('Ali'))
cust.append(Customer('Ahmed'))
cust.append(Customer('Zain'))
cust.append(Customer('Abdullah'))
cust.append(Customer('Zaid'))
cust.append(Customer('Muhammad'))
cust.append(Customer('Shafiq'))
cust.append(Customer('Osama'))
cust.append(Customer('Shan'))
cust.append(Customer('Uzair'))
cust.append(Customer('Farhan'))
cust.append(Customer('Faruq'))
cust.append(Customer('Sajid'))
cust.append(Customer('Wali'))
cust.append(Customer('Zee'))
cust.append(Customer('Hamdan'))

barber = Barber()

barberShop = BarberShop(barber)
barberShop.openShop()


while len(cust) > 0:
    c = cust.pop(-1)	
    #New customer enters the barbershop
    barberShop.enterBarberShop(c)
    customerInterval = random.randrange(customerIntervalMin,customerIntervalMax+1)
    time.sleep(customerInterval)
