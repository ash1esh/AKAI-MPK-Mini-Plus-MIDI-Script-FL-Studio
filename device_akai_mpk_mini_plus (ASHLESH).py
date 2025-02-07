# name=Akai MPK Mini Plus
# supportedDevices=MPK mini Plus
# version=1.0.1
# owner=ashlesh

import transport, general, mixer, midi, device

BUTTON_PREVIOUS = 0x73
BUTTON_NEXT = 0x74
BUTTON_STOP = 0x75
BUTTON_PLAY = 0x76
BUTTON_RECORD = 0x77

def ToggleLED(ledID, on):
    onVal = 1 if on else 0
    arr = [0x90, ledID, onVal]
    device.midiOutSysex(bytes(arr))


def OnControlChange(event):
    event.handled = False
    if event.data2 > 0:
        if event.data1 == BUTTON_PREVIOUS or event.data1 == BUTTON_NEXT:
            should_forward = event.data1 == BUTTON_NEXT
            song_pos = transport.getSongPos(midi.SONGLENGTH_ABSTICKS)
            
            if should_forward:
                new_song_pos = song_pos + general.getRecPPQ()
            else:
                new_song_pos = song_pos - general.getRecPPQ()

            print(f'{"Forwarding" if should_forward else "Rewinding"} by one beat')
            transport.setSongPos(new_song_pos, midi.SONGLENGTH_ABSTICKS)
        elif event.data1 == BUTTON_PLAY:
            print(f'{"Paused" if transport.isPlaying() else "Started"} playback')
            transport.start()
        elif event.data1 == BUTTON_STOP:
            print('Stopped playback')
            transport.stop()
        elif event.data1 == BUTTON_RECORD:
            print(f'{"Disabled" if transport.isRecording() else "Enabled"} recording')
            transport.record()
        else:
            return
        event.handled = True
        

def OnRefresh(flags):
    if flags & midi.HW_Dirty_LEDs:
        # if flag HW_Dirty_LEDs set. Includes various changes in FL Studio which require update of controller leds (e.g. play/stop/record)
        if transport.isPlaying():
            ToggleLED(BUTTON_PLAY, on=True)
            ToggleLED(BUTTON_STOP, on=False)
        else:
            ToggleLED(BUTTON_PLAY, on=False)
            ToggleLED(BUTTON_STOP, on=True)

        if transport.isRecording():
            ToggleLED(BUTTON_RECORD, on=True)
        else:
            ToggleLED(BUTTON_RECORD, on=False)