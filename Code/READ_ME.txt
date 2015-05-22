################################## INSTRUCTIONS ####################################
From virtual machene, first, make sure you don't have a database called db_flyright
you want to keep. Then just click launchFlyRight.py. 
The program in still dependent on having the username set to "root" with password 
"Redfox1!", as in virtual machenes.

Click new reservation on tab 1 to try inputing some reservations. Note on flight 
search - we don't have that many flights! If you can't find one, try going from 
Dallas to LA. Note that the search will return all flights regardless of date, as 
I dsabled this filter as again,  not that much data in database! 

On tab 1 you can also search for existing reservations by reservation id or name+
zip code. You can search for what you entered, or one I know I have is res#48,
first:Joe last:Blow zip:55555


################################ FILES CHANGED #####################################

launchFlyRight.py - completed making tables dynamically populate data. Made changes
to ensure recording data in time needed for queries. Connected with connectDB file 
and designed algorithms to insert, delete, update, or select data in correct order and
by correct relationship. Connected db_flyright_create module to create flyright database
on systems its' not installed.

connectDB.py - Wrote functions to insert, delete, update, or select data to create 
functionality of:
           1) Insert new reservation information
           2) Cancel a reservation
           3) Retrieve Information on a reservation by varius search criteria
           4) Search for a flight matching parameters given throughout app

db4.sql - created a database to store data for and from an airline's
resercation system. Database is in 3rd normal form to allow many flights for many 
passengers for one reservation. Also allows recursion on flight.depart_airport_id=
flight.arrive_airport_id to allow searching for legs of flights.

db_flyright_create.py - processed a sqldump into a py file that will create and populate
db_flyright so prgram can be run without manual installation from source

################################## TO DO, still =( #################################
launchFlyRight.py - Big one - I haven't finished recording return flights. 
Also, there are still some bugs you will find, such as errors on asking for a new return 
date on one way flights. A few missing dialogs on payment page. 

############################# STUFF I HAD TO GIVE UP ON FOR NOW #####################
Modify reservation - release 1 will require cancelling and making a new reservation.

Automatic price adjustments - by date from flight and customer rateCodes. Version 1 will 
require manual database entries in rate table or modification of rate id associated with 
flight.

Automatic caluclation of price, distance, and leg options by data being stored in nodes
in a bidirectional graph class - I faked it my best with the sql 8)



