#/usr/bin/env python3
#coding=utf8

import gi, os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import config, translate
import datetime

def request_translate():
    input = inputentry.get_text().strip()
    if(len(input)==0):
        return
    else:
        show_hint(0, "Translate start ...")
        result,ok = translate.translate(input)
        displaylabel.set_text(result)
        show_hint(0, "Translate ... end")
        inputentry.set_text("")
        show_hint(0 if(ok) else 1, "Translate ... %s" % ("OK" if(ok) else "Failed"))
        if(ok and autosavebtn.get_active()):
            if(not os.path.isdir(config.storagePath)):
                return
            fn = datetime.datetime.now().strftime('%Y-%m')
            file = "%s/word-%s.md" % (config.storagePath, fn)

            addtoc = False if(os.path.exists(file)) else True

            with open(file, "a") as f:
                if(addtoc):
                    f.write("# %s\n\n" % fn)
                    f.write("[TOC]")
                    f.write("\n\n")
                f.write(result)
                f.write("\n\n")
                f.close()
                show_hint(0, "Translate and save ... OK")


class Handler:
    def on_toggleaction_toggled(self, button):
        config.setAutoSave(button.get_active())

    def on_transbtn_clicked(self, button):
        request_translate()
    
    def on_settingsbtn_clicked(self, button):
        if(settingbox.get_property("visible")):
            settingbox.hide()
        else:
            settingentry.set_text(config.getStoragePath())
            settingbox.show()


    def on_dirselectbtn_clicked(self, button):
        origin = config.getStoragePath()
        filechooserdialog.set_filename(origin)
        res = filechooserdialog.run()
        if(res == Gtk.ResponseType.OK):
            new = filechooserdialog.get_filename()
            settingentry.set_text(new)
        filechooserdialog.hide()

    def on_settings_clicked(self, button):
        new = settingentry.get_text().strip()
        if(len(new) > 0 and os.path.exists(new) and os.path.isdir(new)):
            config.setStoragePath(new)
            show_hint(0, "Set markdown record storage to %s" % new)

    def on_window_destroy(self, *args):
        filechooserdialog.destroy()
        Gtk.main_quit(*args)

    def on_inputentry_key_press_event(self, entry, key):
        if(36 == key.get_keycode()[1]):
            request_translate()

    def on_settingentry_key_press_event(self, entry, key):
        if(key.get_keycode()==36):
            pass

def show_hint(msgtype, msg):
    statusbar.push(0, ("%s: %s") % ("Error" if(msgtype!=0) else "Info", msg))

builder = Gtk.Builder()
builder.add_from_file("layout.xml")
builder.connect_signals(Handler())

window = builder.get_object("window")
screen = window.get_screen()
window.move((screen.width()-window.get_size()[0]),(screen.height()-window.get_size()[1]))

autosavebtn = builder.get_object("autosavebtn")
autosavebtn.set_active(config.isAutoSave())

displaylabel = builder.get_object("displaylabel")
inputentry = builder.get_object("inputentry")
transbtn = builder.get_object("transbtn")

settingbox = builder.get_object("settingbox")
settingentry = builder.get_object("settingentry")
settingentry.set_text(config.getStoragePath())
statusbar = builder.get_object("statusbar")

filechooserdialog = builder.get_object("filechooserdialog")
filechooserdialog.set_transient_for(window)
filechooserdialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                   "Select", Gtk.ResponseType.OK)

window.show_all()
inputentry.grab_focus()
settingbox.hide()
Gtk.main()
