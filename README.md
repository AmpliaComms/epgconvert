# epgconvert

DIRECTORY STRUCTURE
	Note the following directory structure is expected from the working directory downwards

	working
	working/config 		This directory holds the config files, currently 
		AmpliaChannels.csv - a csv file with the ID of the channel, and the old CallSign used in the ZW2.x xml files
		graceNoteZappwareGenreMatch.csv - a csv file with the GraceNote GenreID, and the TVAnywhere GenreID
		
	working/graceNoteInputFiles - This directory  holds the GraceNote On_Car_sources file	
		currently it is called on_car_samp_tv_sources_v22_current.xml. This name will probably change when the production files are available
		If it is changed it will need to be changed in the code, or we could write a config file which maps the new name and read it
		when the program is run.
		Note, currently the other two GraceNote on_car files for program and schedules are also loaded here, but those are not 
		used by the python script, as the data from them is acquired using baseX.
		
	working/zappware4Output - This directory is for the output xml epg files in the TVAnywhere format for Zappware 4, and for each channel
		a list of the image files needed for that channel

	working/zappware4Output/xml - This directory is for the output xml epg files in the TVAnywhere format for Zappware 4

	working/zappware4Output/images - This directory is for Zappware 4 outut files for each channel containing the images required for that channel

	working/zappware2Output/xml - This directory is for the output xml epg files in the TVAnywhere format for Zappware 2

	working/zappware2Output/images - This directory is for Zappware 2 outut files for each channel containing the images required for that channel

RE BASEX.
	BaseX XML database is used by the program please ensure that 
	pip install basexclient 
	has been used to add the library to the python environment

	The python script is expecting the following BaseX databases to be available on the localhost server
	GraceNotePrograms - currently created from the on_car_samp_tv_programs_v22_yyyymmdd.xml
	GraceNoteSchedules - currently created from the on_car_samp_tv_schedules_v22_yyyymmdd.xml

	These must be loaded separately prior to running this python script.

	BaseXServer must also be running on the localhost server.
	
OTHER LIBRARIES TO BE LOADED.
	pip install xmltodict
	pip install lxml
	
NOTE
linux diving script files which would reside in the directory above the working directory have been placed in the scripts directory of this repository.


