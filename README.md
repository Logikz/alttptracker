# About
This is a forked implementation of BigDunka's A Link to the Past Randomizer tracker to include a python webservice to
offer predictions should the player load a spoiler log.  This was part of a class project for my Master's program and my
goal is to extract the python service into its own project to possibly serve as a web endpoint
for online simulators or to be played with offline.

# Installation
## Tracker
The tracker does not require any special installation, it runs with native HTML and javascript.
## Webservice
The python(3) webservice is set up to run on Flask. Installation can be done with pip with the following packages:
 - flask
 - flask-cors
 
 There are some additional utility files located in the python folder used in saving/loading/mangling data.
 If you want to run these files you'll need to additionally install.
 - pyarrow
 
 # Running
 The tracker can be opened using index.html.  The seeds were generated using an Open world state with 7 crystals to open
 ganon's tower and 7 crystals to defeat ganon.  Other game types could have seeds generated though, and just as easily
 trained and predicted using this application with minor modifications.
 
 In order to use the predictive services, you'll need to generate a spoiler log of your game and upload it.  So be sure
 to specify the "Use Spoiler Log" setting to "Yes".  I'd recommend removing the option for spheres as it just takes up a
 lot of space.
 
 ## Webservice
 The webservice runs on flask and can be started with a simple
 
  `python alttpr_predictive_service.py`
 
 The webservice can be killed with ctrl+c.
  
 # Data
 The data for the predictive service is compressed and stored as a parquet file.  The webservice handles loading this file
 on startup, and has it ready in memory for each API request.
 
 If you want to download the entire postgres database, you can do so here: https://drive.google.com/file/d/15SZwESI1fAZyY6mP1Yms0nF1brwfwlzv/view?usp=sharing.
 
 Installation and setup of postgres is outside the scope of this README.  There are some python files included
 that can interact with the postgres table to generate the data used by the predictive service.
 
 # Simulating
 A sample spoiler log is provided in the data folder, but feel free to generate your own
 https://alttpr.com/en/randomizer
 
 
 # Known Bugs
 The tracker expects the predictive service to be running on local host for now.
 
 There is a known issue where if a dungeon is accessible, it assumes that every chest is available
 due to the dungeon chest logic being tightly coupled with the colorization of dungeons.  So this could
 lead to some games where for instance, turtle rock is fully accessible without fire rod, which
 might lead the predictive service to clear out all the chests in the dungeon, which can cause the game state
 to become "out of logic".
 
 Currently the predictive service does not use location distance to weight routing decisions, so simulations
 will play out as if link is teleporting to the most likely location.  
 