#/usr/bin/env python3
#coding=utf8

import gi, os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import config, translate
import datetime
import asyncio
from concurrent.futures import Executor,ThreadPoolExecutor

pool = ThreadPoolExecutor(3)

async def request_translate():
    global pool
    input = inputentry.get_text().strip().lower()
    if(len(input)==0):
        return
    else:
        show_hint(0, u"翻译开始 ... 请等待 ...")
        pool.submit(translate.translate)

        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(pool, translate.translate, input),
        ]
        completed, pending = await asyncio.wait(tasks, timeout=2500)
        results = [t.result() for t in completed]

        if(results is None or len(results)==0):
            show_hint(u"翻译 ... 失败")
        
        result, ok = results[0]

        textview.get_buffer().set_text(result)
        show_hint(0, u"翻译 ... 完成")
        inputentry.set_text("")
        show_hint(0 if(ok) else 1, u"翻译 ... %s" % (u"成功" if(ok) else u"失败"))
        if(ok and autosavebtn.get_active()):
            if(not os.path.isdir(storagePath)):
                return
            fn = datetime.datetime.now().strftime('%Y-%m')
            file = "%s/word-%s.md" % (storagePath, fn)
            addtoc = False if(os.path.exists(file)) else True

            try:
                with open(file, "a") as f:
                    if(addtoc):
                        f.write("# %s\n\n" % fn)
                        f.write("[TOC]")
                        f.write("\n\n")
                    f.write(result)
                    f.write("\n\n")
                    f.close()
                    show_hint(0, u"翻译并保存 ... 成功")
            except:
                show_hint(1, u"翻译并保存 ... 失败")

def asynctranslate():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(request_translate())


class Handler:
    def on_toggleaction_toggled(self, button):
        config.setAutoSave(button.get_active())

    def on_transbtn_clicked(self, button):
        asynctranslate()
    
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
        global storagePath
        new = settingentry.get_text().strip()
        if(len(new) > 0 and os.path.exists(new) and os.path.isdir(new)):
            config.setStoragePath(new)
            storagePath = new
            show_hint(0, u"设置Markdown存储路径 ... 失败")

    def on_window_destroy(self, *args):
        filechooserdialog.destroy()
        loop = asyncio.get_event_loop()
        loop.close()
        Gtk.main_quit(*args)

    def on_inputentry_key_press_event(self, entry, key):
        if(36 == key.get_keycode()[1]):  
            asynctranslate()

    def on_settingentry_key_press_event(self, entry, key):
        if(key.get_keycode()==36):
            pass

def show_hint(msgtype, msg):
    statusbar.push(0, (u"%s： %s") % (u"错误" if(msgtype!=0) else u"消息", msg))

os.chdir(os.path.dirname(os.path.abspath(__file__)))

builder = Gtk.Builder()
builder.add_from_file("layout.xml")
builder.connect_signals(Handler())

window = builder.get_object("window")
screen = window.get_screen()
window.move((screen.width()-window.get_size()[0]),(screen.height()-window.get_size()[1]))

autosavebtn = builder.get_object("autosavebtn")
autosavebtn.set_active(config.isAutoSave())

textview = builder.get_object("textview")
inputentry = builder.get_object("inputentry")
transbtn = builder.get_object("transbtn")

settingbox = builder.get_object("settingbox")
settingentry = builder.get_object("settingentry")
storagePath = config.getStoragePath()
settingentry.set_text(storagePath)
statusbar = builder.get_object("statusbar")

filechooserdialog = builder.get_object("filechooserdialog")
filechooserdialog.set_transient_for(window)
filechooserdialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                   "Select", Gtk.ResponseType.OK)

window.show_all()
inputentry.grab_focus()
settingbox.hide()
Gtk.main()
