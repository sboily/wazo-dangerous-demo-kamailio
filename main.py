#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os 

from wazo import Wazo


players = {}


def call_entered(data):
    global players

    call_id = data['call']['id']
    caller_id_number = data['call']['caller_id_number']
    playback = {'uri': 'sound:confbridge-join'}
    wazo.ctid_ng.applications.send_playback(wazo.application_uuid, call_id, playback)
    if not players.get(caller_id_number):
        players[caller_id_number] = 0
    
def stt(data):
    global players

    call_id = data['call_id']
    if not call_id:
        return
    caller_id_number = wazo.ctid_ng.calls.get_call(call_id).get('caller_id_number')
    words = data['result_stt'].split()
    players[caller_id_number] += len(words)

    os.system('clear')
    for player in players:
        print('{}: {}'.format(player, players[player]))

wazo = Wazo('config.yml')
wazo.on('application_call_entered', call_entered)
wazo.on('stt', stt)
wazo.run()
