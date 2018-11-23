# -*- coding: utf-8 -*-
""" Main program which takes GraceNote ON format files and converts them
    to TVAnywhere format for Zappware 4.0 as well as the format for Zappware 2.x
       
"""
from datetime import date, timedelta
import os
import csv
import xmltodict
from epg_event_modules import get_event_data
from epg_event_modules import create_root
from epg_event_modules import create_main_tables
from epg_event_modules import insert_service_info_table
from epg_event_modules import handle_event
from epg_event_modules import finally_write_xml_file
from epg_event_modules import get_service_info
from epg_event_modules import get_list_of_channels
from epg_event_modules import get_list_of_events_objects
from epg_event_modules import write_unique_sort_file
from zw2_functions import create_root_zw2
from zw2_functions import write_zw2_channel_info





####Start of Program
if __name__ == "__main__":

#Set up for tranparent running on Windows machines at home and laptop as well as linux

    if os.name == 'nt':
        if os.getlogin() == 'trevo':#laptop
            BASEDIRECTORY =\
                "C:/Users/Trevo/Dropbox/DataToDecisions/MassyComms/Amplia/Gracenote/working"
        else:
            if os.getlogin() == 'Dada':#Desktop at home
                BASEDIRECTORY =\
                    "C:/Users/Dada/Dropbox/DataToDecisions/MassyComms/Amplia/Gracenote/working"
    else:#Linux
        BASEDIRECTORY = "/home/tdeane/TVAnywhere/working"

#setup environment to go through files for catch up as well as going forward if not already in file.
    NUMBER_FORWARD_DAYS = 0
    NUMBER_CATCHUP_DAYS = 0


#Set up variables to either write xml namespaces and encoding type or not
#Note by default everything was for Zappware 4 format, if for Zappware 2 then it has zW2
    CLEANUP_NAMESPACES = False
    XML_DECLARATION = True
    ZW2CLEANUP_NAMESPACES = True
    ZW2XML_DECLARATION = False
#Change to working directory
    os.chdir(BASEDIRECTORY)
#Read genre Cross reference file which matches GraceNote GenreID to TVAnywhere GenreID
    try :
        with open('config/graceNoteZappwareGenreMatch.csv', mode='r',
                  newline=None, encoding="utf-8") as infile:
            reader = csv.reader(infile)
            GENREMATCH = {rows[0]:rows[1] for rows in reader}
            infile.close()
    except IOError:
        print(":I/O Error Genre Match file graceNoteZappwareGenreMatch.csv - not found")
        raise
#Read list of Amplia Channels from file in config dirctory. It also reads in the 
#        corresponding callSign as used in Zappware 2.x epg files in order to be able
#        to continue using the same ZW2 call signs in the zw2 epg xml files created.
    try:
        with open('config/AmpliaChannels.csv', mode='r', newline=None, encoding="utf-8") as infile:
            reader = csv.reader(infile)
            amplia_channels = {rows[0]:rows[1] for rows in reader}
            infile.close()
    except IOError:
        print(":I/O Error Genre Match file AmpliaChannels.csv - not found")
        raise
#set reference day
    reference_day = date.today()
#will need logic to select source file for day
    SourceFilename = 'graceNoteInputFiles/on_car_samp_tv_sources_v22_current.xml'
#set up array of days from - catchup days to + number of forward days in EPG
    day_number = -NUMBER_CATCHUP_DAYS
    list_of_days = []
    while day_number <= NUMBER_FORWARD_DAYS:
        list_of_days.append(reference_day + timedelta(days=day_number))
        day_number = day_number + 1

    for schedule_day in list_of_days:
#For each day get a list of channels in the source file for that day

        channel_list_gn = get_list_of_channels(schedule_day)
# this variable has a list of the channels to be processed as read from config file
        channel_list = amplia_channels.keys()
#  On first day through here we need to open for writing
#     the file for the effective day and channel
# Using the objectify library to create the xml files

#    we need to create the main static tables in the objectify object
#   we also need to write the service information table at this time
#    insertServieInformationTable(channel)


        for channel_element in channel_list:
            if channel_element in channel_list_gn:
#Get list of all the events for that channel for that day
                gn_events_for_channel_day_xml = get_list_of_events_objects(channel_element)
    #transform the xml retrieved into a dict structure with all the tags and attributes
                gn_events_for_channel_day = xmltodict.parse(gn_events_for_channel_day_xml)
                print(channel_element)    #print channel that we are working on
    #    we need to create the root of the objectify object for both Zappware 4 file and Zappware 2 file
                root_of_objectivy_object = create_root()
                root_zw2 = create_root_zw2()
    #start forming an array structure for the xml objects
                ProgramInformationArray = []
    #Get service information info for that channel
                service_info = get_service_info(channel_element, SourceFilename)
    #  we need to create the main static tables in the objectify object
                main_tables = create_main_tables(root_of_objectivy_object, channel_element)
    # write the ServiceInformationTable (ZW4)
                insert_service_info_table(main_tables["service_information_table"], service_info)
    #write the ChannelInformation (ZW2)
                write_zw2_channel_info(root_zw2, service_info, amplia_channels)
    #set up file names for the output files.
                filename_xml = 'zappware4Output/xml/' +channel_element +\
                    "_" + reference_day.strftime('%Y%m%d') +'.xml'
                filename_zw2_xml = 'zappware2Output/xml/' + amplia_channels[service_info["serviceId"]] +\
                    "_" + reference_day.strftime('%Y%m%d') +'.xml'
                filename_img = 'zappware4Output/images/' +channel_element +\
                    "_" + reference_day.strftime('%Y%m%d') +'.txt'
                filename_zw2_img = 'zappware2Output/images/' + amplia_channels[service_info["serviceId"]] +\
                    "_" + reference_day.strftime('%Y%m%d') +'.txt'
    #set up variables to hold programIDs and groupIDs used, as well as graphic assets needed.
                program_ids_already_used = []
                group_ids_already_used = []
                graphics_assets = []
                zw2_graphics_assets = []
                program_information_index = 0
    #For each event on the day
                for element in gn_events_for_channel_day['xml']['event']:
    #for each event on the channel for the day get event data into data structure from xml file
                    event_data = get_event_data(element)
#                    print(event_data['program_id']) #print programId being handled
    
                    handle_event(main_tables, event_data, program_ids_already_used,
                                 group_ids_already_used, GENREMATCH, root_zw2,
                                 service_info, graphics_assets, zw2_graphics_assets,
                                 amplia_channels)
                #PLACE TO CALL FUNCTION TO WRITE FOR SINGLE EVENT
                write_unique_sort_file(filename_img, graphics_assets, BASEDIRECTORY)
                write_unique_sort_file(filename_zw2_img, zw2_graphics_assets, BASEDIRECTORY)
                finally_write_xml_file(root_of_objectivy_object, filename_xml,
                                       BASEDIRECTORY, CLEANUP_NAMESPACES, XML_DECLARATION)
                finally_write_xml_file(root_zw2, filename_zw2_xml, BASEDIRECTORY,
                                       ZW2CLEANUP_NAMESPACES, ZW2XML_DECLARATION)
            else:
                print("Channel - "+ channel_element+" Not in Gracenote repository")
    
        #        del eventRating
        #        del eventRatingBody
        #        del tvquals
        #        del netSynSourceForEvent
        #        del netSynTypeForEvent
