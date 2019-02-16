from sqlalchemy.orm import sessionmaker
from database_setup import engine, Base, Category, Person, User

DBSession = sessionmaker(bind=engine)
session = DBSession()

admin = User(email="mohitlal@outlook.com")
mohit = User(email="mohitlal31@gmail.com")

plumber = Category(name="Plumber", user=admin)
carpenter = Category(name="Carpenter", user=admin)
electrician = Category(name="Electrician", user=admin)
mechanic = Category(name="Mechanic", user=mohit)

plumber1 = Person(name="Ajay Venkatesan",
                  address="""Defence Colony, 100 Feet Road, Indiranagar""",
                  mobile="99410369", category=plumber, user=admin)
plumber2 = Person(name="Meghana Raju",
                  address="""75 /, Girls School Road, Mavalli""",
                  mobile="95120252", category=plumber, user=admin)
plumber3 = Person(name="Abhimanyu Sem",
                  address="""C/1, Jivanjyoti Bldg, 18/2, \
Cawasji Patel Street, Above Bank Of Rajasthan, Fort""",
                  mobile="23623192",
                  category=plumber, user=admin)
plumber4 = Person(name="Rajesh Chauhan",
                  address="""Shop No.10, 25/26, Manish Sunflower, 4 Bungalow, \
Opp. St. Louis Convent., Andheri (west)""",
                  mobile="99043763",
                  category=plumber, user=admin)
plumber5 = Person(name="Ishan Kapoor",
                  address="""252 /, B Wing, Sector-, Big Splash, Vashi,\
Navi Mumbai""",
                  mobile="44711082",
                  category=plumber, user=mohit)


carpenter1 = Person(name="Anika Patel",
                    address="""4135  A, Naya Bazar""",
                    mobile="14952699",
                    category=carpenter, user=admin)
carpenter2 = Person(name="Abhinav Tata",
                    address="""50 /a, Pankaj Makarand Soc, Senpati Bapat Marg,\
Dadar (west)""",
                    mobile="19446961",
                    category=carpenter, user=admin)
carpenter3 = Person(name="Rajesh Patil",
                    address="""Shop-6, Payawadi, Service Rd, W.exp. Highway,\
Vile Parle(e)""",
                    mobile="85453287",
                    category=carpenter, user=admin)
carpenter4 = Person(name="Vivaan Pillai",
                    address="""704  / , Cotton Exchange Ldg, Kalbadevi Road,\
Kalbadevi""",
                    mobile="93706299",
                    category=carpenter, user=mohit)


electrician1 = Person(name="Aditya Shah",
                      address="""516 , Mj Market, Chandra Chowk, Kalbadevi""",
                      mobile="67409803",
                      category=electrician, user=admin)
electrician2 = Person(name="Vihaan Sarin",
                      address="""317 - Morach Plaza , Sai Chambers, CBD,\
Konkan Bhawan, Belapur(cbd), Navi Mumbai""",
                      mobile="82835821",
                      category=electrician, user=admin)
electrician3 = Person(name="Chirag Mistry",
                      address="""21 , Arunodaya Shopping Centre,\
Near Ajanta Cinema, Borivli (w)""",
                      mobile="49296703",
                      category=electrician, user=admin)
electrician4 = Person(name="Sai Rangan",
                      address="""A 397, Shastri Nagar""",
                      mobile="32399203",
                      category=electrician, user=admin)
electrician5 = Person(name="Vibhore Dutta",
                      address="""36 ,basement, Mirza Shopping Center,\
Bazar Ward, Manvel Pada Rd, Virar""",
                      mobile="97600619",
                      category=electrician, user=mohit)


mechanic1 = Person(name="Arnav Gupta",
                   address="""176 , Udyog Bhavan, Sonawala Rd, Goregaon (e)""",
                   mobile="59396573",
                   category=mechanic, user=admin)
mechanic2 = Person(name="Parakram Lobo",
                   address="""B-6, Ramanashree Chambers, Lady Curzen Road""",
                   mobile="99938972",
                   category=mechanic, user=admin)
mechanic3 = Person(name="Aradhya Das",
                   address="""112 , Appaavu Garamani Street Mount Road""",
                   mobile="85260798",
                   category=mechanic, user=admin)
mechanic4 = Person(name="Arjun Jaiteley",
                   address="""126 , Oshiwara, Mhada Commercial Complex,\
Link Road Extn, Jogeshwari (west)""",
                   mobile="43197813",
                   category=mechanic, user=admin)
mechanic5 = Person(name="Pranav Shah",
                   address="""57 , Agrawal House, K N Road,\
Opp Hanuman Temple, Masjid Bunder (east)""",
                   mobile="20543993",
                   category=mechanic, user=mohit)

session.add(admin)
session.add(mohit)

session.add_all([plumber, carpenter, electrician, mechanic])
session.add_all([plumber1, plumber2, plumber3, plumber4, plumber5])
session.add_all([carpenter1, carpenter2, carpenter3, carpenter4])
session.add_all([electrician1, electrician2, electrician3, electrician4,
                electrician5])
session.add_all([mechanic1, mechanic2, mechanic3, mechanic4, mechanic5])

session.commit()
