#!/usr/bin/env python2
# -*-: coding utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
import hermes_python
import io
import os
import sys
import json

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section: {option_name : option for option_name, option in self.items(section)} for section in self.sections()}

class UserInfo(user, assistant):

    def __init__(self, user, assistant):
        self.user = user
        self.assistant = assistant
        initDb(self)

    def initDb(self):
        with open('mockdb.json') as f:
            self.MOCKDATABASE = json.load(f)

    def selectUserInfo(self, user, info):
        return self.MOCKDATABASE[user][info]

    def getUserIdentity(self, user):
        if user == "you":
            return self.assistant
        elif user == "I":
            return self.user

    def speakUserInfo(self, user, type, value):
        if user == self.assistant:
            if type == "identity":
                return "{}, your assistant."
            elif type == "name":
                return "I'm {}."
            elif type == "birthday":
                return "{}"
            elif type == "occupation":
                return "I am {}"
            elif type == "job":
                return "I work at {}"
            elif type == "profession":
                return "I am a {}"
            elif type == "employer":
                return "I work for {}"
        elif user == self.user:
            if type == "identity":
                return "You're {}"
            elif type == "name":
                return "Your name is {}."
            elif type == "birthday":
                return "{}"
            elif type == "occupation":
                return "You're a {}"
            elif type == "job":
                return "You work at {}"
            elif type == "profession":
                return "I am a {}"
            elif type == "employer":
                return "I work for {}"

def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()

def getUser(snips):
    if snips.slots.user:
        res = snips.slots.user[0].slot_value.value.value
        return unicode(res)
    return None

def getInfo(snips):
    if snips.slots.info:
        res = snips.slots.info[0].slot_value.value.value
        return unicode(res)
    return None

def queryUserInfo(hermes, intent_message):
    user = getUser(intent_message)
    info = getInfo(intent_message)
    value = hermes.skill.getUserInfo(user, info)
    res = hermes.skill.speakUserInfo(user, info, value)
    current_session_id = intent_message.session_id
    hermes.publish_end_session(current_session_id, res.decode("latin-1

if __name__ == "__main__":
    config = read_configuration_file("config.ini")
    user = config.get("secret").get("username")
    assistant = config.get("secret").get("assistantname")

    if USER is None:
        print "No username set in config.ini, you must setup a username for this skill to work"
    elif ASSISTANT is None:
        print "No assistantname set in config.ini, you must setup a assistantname for this skill to work"

    skill = UserInfo(user, assistant)

    with Hermes(MQTT_ADDR.encode("ascii")) as h:
        h.skill = skill
        h.subscribe_intent("getUserInfo",
                           getUserInfo) \
        .loop_forever()
