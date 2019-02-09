from sqlalchemy.orm import sessionmaker
from database_setup import engine, Base, Category, Person

DBSession = sessionmaker(bind=engine)
session = DBSession()

plumber = Category(name="Plumber")
carpenter = Category(name="Carpenter")
electrician = Category(name="Electrician")
mechanic = Category(name="Mechanic")

plumber1 = Person(name="Ajay Venkatesan",
                  address="""Defence Colony, 100 Feet Road, Indiranagar""",
                  mobile="9941036952", category=plumber)
plumber2 = Person(name="Meghana Raju",
                  address="""75 /, Girls School Road, Mavalli""",
                  mobile="9512025206", category=plumber)
plumber3 = Person(name="Abhimanyu Sem",
                  address="""C/1, Jivanjyoti Bldg, 18/2, \
Cawasji Patel Street, Above Bank Of Rajasthan, Fort""",
                  mobile="2362319257",
                  category=plumber)
plumber4 = Person(name="Rajesh Chauhan",
                  address="""Shop No.10, 25/26, Manish Sunflower, 4 Bungalow, \
Opp. St. Louis Convent., Andheri (west)""",
                  mobile="9904376375",
                  category=plumber)
plumber5 = Person(name="Ishan Kapoor",
                  address="""252 /, B Wing, Sector-, Big Splash, Vashi,\
Navi Mumbai""",
                  mobile="4471108256",
                  category=plumber)


carpenter1 = Person(name="Anika Patel",
                    address="""4135  A, Naya Bazar""",
                    mobile="1495269973",
                    category=carpenter)
carpenter2 = Person(name="Abhinav Tata",
                    address="""50 /a, Pankaj Makarand Soc, Senpati Bapat Marg,\
Dadar (west)""",
                    mobile="1944696431",
                    category=carpenter)
carpenter3 = Person(name="Rajesh Patil",
                    address="""Shop-6, Payawadi, Service Rd, W.exp. Highway,\
Vile Parle(e)""",
                    mobile="8545312287",
                    category=carpenter)
carpenter4 = Person(name="Vivaan Pillai",
                    address="""704  / , Cotton Exchange Ldg, Kalbadevi Road,\
Kalbadevi""",
                    mobile="9370836299",
                    category=carpenter)


electrician1 = Person(name="Aditya Shah",
                      address="""516 , Mj Market, Chandra Chowk, Kalbadevi""",
                      mobile="6749509803",
                      category=electrician)
electrician2 = Person(name="Vihaan Sarin",
                      address="""317 - Morach Plaza , Sai Chambers, CBD,\
Konkan Bhawan, Belapur(cbd), Navi Mumbai""",
                      mobile="8283523821",
                      category=electrician)
electrician3 = Person(name="Chirag Mistry",
                      address="""21 , Arunodaya Shopping Centre,\
Near Ajanta Cinema, Borivli (w)""",
                      mobile="4920096703",
                      category=electrician)
electrician4 = Person(name="Sai Rangan",
                      address="""A 397, Shastri Nagar""",
                      mobile="3239179203",
                      category=electrician)
electrician5 = Person(name="Vibhore Dutta",
                      address="""36 ,basement, Mirza Shopping Center,\
Bazar Ward, Manvel Pada Rd, Virar""",
                      mobile="9797600619",
                      category=electrician)


mechanic1 = Person(name="Arnav Gupta",
                   address="""176 , Udyog Bhavan, Sonawala Rd, Goregaon (e)""",
                   mobile="5933896573",
                   category=mechanic)
mechanic2 = Person(name="Parakram Lobo",
                   address="""B-6, Ramanashree Chambers, Lady Curzen Road""",
                   mobile="9994138972",
                   category=mechanic)
mechanic3 = Person(name="Aradhya Das",
                   address="""112 , Appaavu Garamani Street Mount Road""",
                   mobile="8547260798",
                   category=mechanic)
mechanic4 = Person(name="Arjun Jaiteley",
                   address="""126 , Oshiwara, Mhada Commercial Complex,\
Link Road Extn, Jogeshwari (west)""",
                   mobile="4317997813",
                   category=mechanic)
mechanic5 = Person(name="Pranav Shah",
                   address="""57 , Agrawal House, K N Road,\
Opp Hanuman Temple, Masjid Bunder (east)""",
                   mobile="2054293993",
                   category=mechanic)

session.add_all([plumber, carpenter, electrician, mechanic])
session.add_all([plumber1, plumber2, plumber3, plumber4, plumber5])
session.add_all([carpenter1, carpenter2, carpenter3, carpenter4])
session.add_all([electrician1, electrician2, electrician3, electrician4,
                electrician5])
session.add_all([mechanic1, mechanic2, mechanic3, mechanic4, mechanic5])

session.commit()
