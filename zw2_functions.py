# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 12:15:16 2018

@author: Trevor Deane
"""
from lxml import objectify
#Zappware 2x specific functions

def create_root_zw2():
    """This function generates the lxml root element for the Zappware 2 xml tree
    It  includes all of the necessary namespaces and returns the root element
    """
    root_zw2 = objectify.Element('tv')
    root_zw2.set('{http://www.w3.org/XML/1998/namespace}lang', 'EN')

    return root_zw2


def get_zw2_channel_data(service_info, amplia_channels):
    """This function takes the service Information dict variable created for ZW4
     and returns relevant channel information in a list variable
    """
    zw2_channel_data = dict()
    zw2_channel_data["channelId"] = service_info["serviceId"]
    zw2_channel_data["displayName"] = service_info["name"]
    if isinstance(service_info["lang"], list):
        zw2_channel_data["displayNameLang"] = service_info["lang"][0]
    else:
        zw2_channel_data["displayNameLang"] = service_info["lang"]
    zw2_channel_data["callSign"] = service_info["callSign"]
    zw2_channel_data["callSign_amplia"] = amplia_channels[service_info["serviceId"]]
    zw2_channel_data["channelUrl"] = ""
    return zw2_channel_data

def write_zw2_channel_info(root_zw2, service_info, amplia_channels):
    """This function takes the Zappware 2 lxml root variable and the specific
    ZW2 service Information dict variable and adds the channel data to the
    lxml object
    """
    zw2_channel_data = get_zw2_channel_data(service_info, amplia_channels)
    channel_tag = objectify.Element("channel")
    root_zw2.append(channel_tag)
    channel_tag.set("id", zw2_channel_data["callSign_amplia"])
    display_name = objectify.SubElement(channel_tag, "display-name")
    display_name._setText(zw2_channel_data["displayName"])
    display_name.set("lang", zw2_channel_data["displayNameLang"])
    channel_tag.Url = zw2_channel_data["channelUrl"]
    return


def get_zw2_image_data(grace_note_dict):
    """This function takes the xmltodict list variable which was created from the
    xml data for the specific programID and checks for images which are
    360x270px and Iconic and creates and returns a dict variable with those images
    references
    """
    zw2_image_data = dict()
    zw2_image_data['imageSource'] = ''
    zw2_image_data['type'] = ''
    try:
        if isinstance(grace_note_dict['xml']['assets']['asset'], list):
            for element in grace_note_dict['xml']['assets']['asset']:
                if element['@width'] == '360' and element['@height'] == '270'\
                and element['@category'] == 'Iconic':
                    zw2_image_data['imageSource'] = element['URI'][7:]
                    zw2_image_data['imageSourceWithDirectory'] = element['URI']
                    zw2_image_data['type'] = '99'
                    return  zw2_image_data
        else:
            if element['@width'] == '360' and element['@height'] == '270'\
            and element['@category'] == 'Iconic':
                zw2_image_data['imageSource'] = element['URI'][7:]
                zw2_image_data['imageSourceWithDirectory'] = element['URI']
                zw2_image_data['type'] = '99'
                return zw2_image_data
        return zw2_image_data

    except (UnboundLocalError, KeyError, IndexError, LookupError, NameError, ValueError):
        return zw2_image_data


def get_zw2_programme_data(b_d_unique, service_info, event_data, grace_note_dict, b_d_synopsis,
                           amplia_channels):
    """This function takes the specific ZW4 dict variables with relevant data
    as well as the xmltodict list variable which was created from the
    xml data for the specific programID returns a dict variable with data required
    to complete the Zappware 2.x programme Data table
    """
    zw2_programme_data = dict()
    zw2_programme_data["startTime"] = event_data['gmt_date_time_start_zw2']
    zw2_programme_data["stopTime"] = event_data['gmt_date_time_end_zw2']
    zw2_programme_data["channel"] = service_info["name"]
    zw2_programme_data["callSign"] = service_info["callSign"]
    zw2_programme_data["callSign_amplia"] = amplia_channels[service_info["serviceId"]]
    zw2_programme_data["recordable"] = "y"
    zw2_programme_data["npvrenable"] = "y"
    zw2_programme_data["id"] = b_d_unique['guid']
    zw2_programme_data["type"] = b_d_unique['BDKeyword']
    zw2_programme_data["programTitle"] = b_d_unique['BDTitle']
    zw2_programme_data["language"] = b_d_unique['BDTitle_att_lang_zw25']
    try:
        zw2_programme_data["programSubTitle"] =\
            grace_note_dict['xml']['episodeInfo']['title']['#text']
        zw2_programme_data["subTitleLanguage"] =\
            grace_note_dict['xml']['episodeInfo']['title']['@lang']
    except (UnboundLocalError, KeyError, IndexError, LookupError, NameError, ValueError):
        zw2_programme_data["programSubTitle"] = ""
        zw2_programme_data["subTitleLanguage"] = ""
#    b_d_synopsis = createbDSynopsis(grace_note_dict)
    try:
        zw2_programme_data["desc"] = b_d_synopsis[0]["b_d_synopsis"]
        zw2_programme_data["descLanguage"] = b_d_synopsis[0]["b_d_synopsis_att_lang_zw25"]
    except (UnboundLocalError, KeyError, IndexError, LookupError, NameError, ValueError):
        zw2_programme_data["desc"] = ''
        zw2_programme_data["descLanguage"] = ''
    zw2_image_data = get_zw2_image_data(grace_note_dict)
    try:
        zw2_programme_data["imageSource"] = zw2_image_data['imageSource']
        zw2_programme_data["imageSourceWithDirectory"] = zw2_image_data['imageSourceWithDirectory']
        zw2_programme_data["imageType"] = zw2_image_data['type']
    except (UnboundLocalError, KeyError, IndexError, LookupError, NameError, ValueError):
        zw2_programme_data["imageSource"] = ''
        zw2_programme_data["imageSourceWithDirectory"] = ''
        zw2_programme_data["imageType"] = ''
    zw2_programme_data["country"] = b_d_unique['BDProductionLocation']
    try:
        zw2_programme_data["seasonNumber"] = int(grace_note_dict['xml']['episodeInfo']['@season'])
    except (UnboundLocalError, KeyError, IndexError, LookupError, NameError, ValueError):
        zw2_programme_data["seasonNumber"] = ""
    try:
        zw2_programme_data["episodeNumber"] = int(grace_note_dict['xml']['episodeInfo']['@number'])
    except (UnboundLocalError, KeyError, IndexError, LookupError, NameError, ValueError):
        zw2_programme_data["episodeNumber"] = ""
    if zw2_programme_data["episodeNumber"] != "":
        if zw2_programme_data["seasonNumber"] != "":
            zw2_programme_data["episodeNum"] = str(zw2_programme_data["seasonNumber"] - 1) +\
                '.' + str(zw2_programme_data["episodeNumber"] -  1) + '.0'
        else:
            zw2_programme_data["episodeNum"] = '0' +\
                    '.' + str(zw2_programme_data["episodeNumber"] -  1) + '.0'
    else:
        zw2_programme_data["episodeNum"] = ""
    zw2_programme_data["episodeSystem"] = "xmltv_ns"
    zw2_programme_data["ratingSystem"] = "DVB"
    zw2_programme_data["minimumAge"] = b_d_unique['BDParentalGuidanceMinimumAge']
    zw2_programme_data["key"] = 'releaseStatus'
    if event_data['quals'].find('New') >= 0:
        zw2_programme_data["value"] = "0"
    else:
        zw2_programme_data["value"] = "1"
    return zw2_programme_data


def write_zw2_programme_info(root_zw2, event_data, b_d_unique, service_info, grace_note_dict,
                             b_d_credits, b_d_synopsis, b_d_genres, zw2_graphics_assets,
                             amplia_channels):
    """This function takes the lxml objectify root object for Zappware 2.x,
    the xmltodict list variable which was created from the xml data for the specific
    programID, various specific ZW4 dict variables with relevant data and the
    zappware 2 variable which holds the running list of the graphics assets
    used and adds the relevant objects to the lxml objectify programme Table. It
    also appends any new images used to the graphics assets used variable
    """
    zw2_programme_data = get_zw2_programme_data(b_d_unique, service_info, event_data,
                                                grace_note_dict, b_d_synopsis,
                                                amplia_channels)
    programme_tag = objectify.Element("programme")
    root_zw2.append(programme_tag)
    programme_tag.set("start", zw2_programme_data["startTime"])
    programme_tag.set("stop", zw2_programme_data["stopTime"])
    programme_tag.set("channel", zw2_programme_data["callSign_amplia"])
    programme_tag.set("recordable", zw2_programme_data["recordable"])
    programme_tag.set("npvrenable", zw2_programme_data["npvrenable"])
    programme_tag.set("id", zw2_programme_data["id"])
    if zw2_programme_data["id"][0:2] == 'SH':
        programme_tag.set("type", 'program')
    elif zw2_programme_data["id"][0:2] == 'EP':
        programme_tag.set("type", 'episode')
    else:
        programme_tag.set("type", '')
#    programme_tag.set("type", zw2_programme_data["type"])
    programme_tag.title = zw2_programme_data["programTitle"]
    programme_tag.title.set("lang", zw2_programme_data["language"])
    if zw2_programme_data["programSubTitle"] != '':
        programme_tag.subTitle = zw2_programme_data["programSubTitle"]
        programme_tag.subTitle.set("lang", zw2_programme_data["subTitleLanguage"])
    programme_tag.desc = zw2_programme_data["desc"]
    programme_tag.desc.set("lang", zw2_programme_data["descLanguage"])
#multiple credits
    programme_tag.credits = ""
#    b_d_credits = createbDCredits(grace_note_dict)
    try:
        for b_d_credits_element in b_d_credits:
            if b_d_credits_element["BDPersonNameRole"].upper() == "PRODUCER":
                objectify.SubElement(programme_tag.credits, 'producer').\
                    _setText(b_d_credits_element["BDPersonNameGivenName"] +\
                             ' ' + b_d_credits_element["BDPersonNameFamilyName"])
            elif b_d_credits_element["BDPersonNameRole"].upper() == "DIRECTOR":
                objectify.SubElement(programme_tag.credits, 'director').\
                    _setText(b_d_credits_element["BDPersonNameGivenName"] +\
                             ' ' + b_d_credits_element["BDPersonNameFamilyName"])
            elif b_d_credits_element["BDPersonNameRole"].upper() == "ACTOR":
                objectify.SubElement(programme_tag.credits, ' actor').\
                    _setText(b_d_credits_element["BDPersonNameGivenName"] +\
                             ' ' + b_d_credits_element["BDPersonNameFamilyName"])
            elif b_d_credits_element["BDPersonNameRole"].upper() == "WRITER":
                objectify.SubElement(programme_tag.credits, 'writer').\
                    _setText(b_d_credits_element["BDPersonNameGivenName"] +\
                             ' ' + b_d_credits_element["BDPersonNameFamilyName"])
    except (UnboundLocalError, KeyError, IndexError, LookupError, NameError, ValueError):
        pass
#    programme_tag.credits.date = "date"
#multiple categories
#    bDGeneres = createbDGenre(grace_note_dict, GENREMATCH)
    try:
        for b_d_generes_element in b_d_genres:
            temp_obj = objectify.SubElement(programme_tag, 'category')
            temp_obj._setText(b_d_generes_element['genreName'])
    #        programme_tag.category = "Category to put here"
            temp_obj.set("lang", "Language")
    except (UnboundLocalError, KeyError, IndexError, LookupError, NameError, ValueError):
        pass

    programme_tag.icon = zw2_programme_data["imageSource"]
    zw2_graphics_assets.append(zw2_programme_data["imageSourceWithDirectory"])
    programme_tag.icon.set("ptype", zw2_programme_data["imageType"])
    programme_tag.country = zw2_programme_data["country"]
    episode_num = objectify.SubElement(programme_tag, "episode-num")

    episode_num._setText(zw2_programme_data["episodeNum"])
    episode_num.set("system", zw2_programme_data["episodeSystem"])
    programme_tag.rating = ""
    programme_tag.rating.set("system", zw2_programme_data["ratingSystem"])
    programme_tag.rating.value = zw2_programme_data["minimumAge"]
    programme_tag.extentionInfo = ""
    programme_tag.extentionInfo.key = zw2_programme_data["key"]
    programme_tag.extentionInfo.value = zw2_programme_data["value"]
    return
