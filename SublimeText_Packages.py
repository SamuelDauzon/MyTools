
import time
import os
import zlib
import zipfile
import gzip
import base64
import unicodedata
import hashlib
import binascii
import subprocess
import sys
import datetime
import operator
import json
import re
import collections

import requests
import sublime, sublime_plugin

sys.setrecursionlimit(10000)

# pi = 4-4/3
# for i in range(1, 10):
#     pi += (4/(i*4+1))-(4/(i*4+3))
#     print("PI ("+str(i-1)+") : "+str(pi))


class TestStCommand(sublime_plugin.TextCommand):

    def run(self, edit):


        selections = self.view.sel()
        for selection in selections:
            new_content = ""
            old_content = str(self.view.substr(selection))
            items = old_content.split("\n")
            items = [x for x in items if x]
            counter = collections.Counter(items)
            counter = dict(counter)
            counter = sorted(counter.items(), key=lambda kv: kv[1], reverse=True)
            new_content = "\n".join([ item[0]+": "+str(item[1]) for item in counter])
            with Edit(self.view) as edit:
                edit.replace(selection, new_content)



class LineFrenquencyCommand(sublime_plugin.TextCommand):
    # { "keys": ["ctrl+shift+l", "ctrl+shift+f"], "command": "line_frenquency", "args": { }  },

    def run(self, edit):
        selections = self.view.sel()
        for selection in selections:
            new_content = ""
            old_content = str(self.view.substr(selection))
            items = old_content.split("\n")
            items = [x for x in items if x]
            counter = collections.Counter(items)
            counter = dict(counter)
            counter = sorted(counter.items(), key=lambda kv: kv[1], reverse=True)
            new_content = "\n".join([ item[0]+": "+str(item[1]) for item in counter])
            with Edit(self.view) as edit:
                edit.replace(selection, new_content)


class SelectToCharCommand(sublime_plugin.TextCommand):
    # {"keys": ["alt+s", "alt+c", "<character>"], "command": "select_to_char", "args": {}},

    def run(self, edit, character=None, only_line=False):
        if not character:
            return None

        region_list = []
        for current_selection in self.view.sel():
            for i in range(0, 500):
                region = sublime.Region(current_selection.begin(), current_selection.end()+i)
                region_str = self.view.substr(region)
                if only_line and region_str and region_str[-1] == "\n":
                    break
                if region_str and region_str[-1] == character:
                    region_list.append(region)
                    break

        if region_list:
            self.view.sel().clear()
            self.view.sel().add_all(region_list)
            sublime.status_message("----- %d region(s) expanded -----" % (len(region_list)))

def file_sha3_256(file_path):
    with open(file_path, 'rb') as f:
        return hashlib.sha3_256(f.read()).hexdigest()



class CharStatCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selections = self.view.sel()
        for selection in selections:
            old_content = str(self.view.substr(selection))
            char_stat = {}
            for char in old_content:
                if char not in char_stat:
                    char_stat[char] = 0
                char_stat[char]+=1
            char_stat = sorted(char_stat.items(), key=lambda kv: kv[1], reverse=True)
            new_content = ''
            new_content = "\n".join([ char[0]+": "+str(char[1]) for char in char_stat])
            with Edit(self.view) as edit:
                edit.replace(selection, new_content)

class CustomMinifyCommand(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        file_path = str(view.file_name())
        if file_path.endswith(('.js', '.css')):
            project_path = file_path
            while not os.path.exists(project_path+os.sep+"minifpy_settings.json") and project_path:
                project_path = os.sep.join(project_path.split(os.sep)[:-1])
            if project_path:
                command = "py "+os.path.join(project_path, "minifpy.py")+" --file="+file_path
                result_code = subprocess.call(command, shell=True)
                if result_code == 0:
                    sublime.status_message("----- Minify done ✅ -----")
                else:
                    sublime.error_message(" ⚠ Minifpy a échoué ⚠")


class CharCodeCommand(sublime_plugin.TextCommand):
    # { "keys": ["alt+c", "alt+c"], "command": "char_code", "args": {}  },
    def run(self, edit, to_base_64=True):
        selections = self.view.sel()
        for selection in selections:
            old_content = str(self.view.substr(selection))
            new_content = ""
            new_content = ";".join([str(ord(x)) for x in old_content])
            with Edit(self.view) as edit:
                edit.replace(selection, new_content)


#import sublime, sublime_plugin
#import base64
class Base64Command(sublime_plugin.TextCommand):
    # { "keys": ["ctrl+shift+b", "ctrl+shift+b"], "command": "base64", "args": { "to_base_64": true}  },
    # { "keys": ["ctrl+shift+b", "ctrl+shift+n"], "command": "base64", "args": { "to_base_64": false}  },
    def run(self, edit, to_base_64=True):
        selections = self.view.sel()
        for selection in selections:
            old_content = str(self.view.substr(selection))
            if to_base_64:
                new_content = base64.b64encode(str(old_content).encode('utf-8')).decode('utf-8')
            else:
                new_content = base64.b64decode(str(old_content).encode('utf-8')).decode('utf-8')
            with Edit(self.view) as edit:
                edit.replace(selection, new_content)


class Categorie():
    titre = ''
    caractere = ''

    def __init__(self, titre, caractere):
        self.titre = titre
        self.caractere = caractere

class NotePrincipaleCommand(sublime_plugin.TextCommand):

    categorie_list = []
    caractere = ""
    titre_list = []

    def run(self, edit, caractere):
        self.categorie_list.append(Categorie(titre = "Général", caractere="-"))
        self.categorie_list.append(Categorie(titre = "Tickets", caractere="#"))
        self.categorie_list.append(Categorie(titre = "Docs", caractere=">"))

        self.caractere = caractere

        contenu_total = sublime.Region(0, self.view.size())
        content = self.view.substr(contenu_total)
        text = str(content)

        caractere = str(caractere)
        p = re.compile('([^'+caractere+']\\'+caractere+'{5,6}[^'+caractere+'].+)[\\n]')
        self.titre_list = re.findall(p, text)
        self.view.window().show_quick_panel(self.titre_list, self.on_done, sublime.MONOSPACE_FONT, 0, self.on_highlighted)

    def on_done(self, search):
        text_search = self.titre_list[search]
        contenu_total = sublime.Region(0, self.view.size())
        content = self.view.substr(contenu_total)
        text = str(content)
        begin = content.find(text_search)
        end = begin + len(text_search)

        target_region = sublime.Region(begin, end)
        self.view.sel().clear()
        self.view.sel().add(target_region)

        # (row,col) = self.view.rowcol(self.view.sel()[0].begin())
        self.view.show_at_center(target_region)
        # self.view.show(target_region)

    def on_highlighted(self, search):
        self.on_done(search)


class PrefereFilesCommand(sublime_plugin.TextCommand):
    def run(self, edit, save, number):
        settings = sublime.load_settings("PrefereFiles.sublime-settings")
        if save:
            value = sublime.ok_cancel_dialog("Etes-vous sûr de vouloir sauvegarder ce fichier en position "+str(number)+" ?")
            if value:
                file_name = str(self.view.file_name())
                settings.set("fichier_prefere_"+str(number), file_name)
                sublime.save_settings("PrefereFiles.sublime-settings")
        else:
            file_name = str(settings.get("fichier_prefere_"+str(number)))
            if file_name!="None":
                self.view.window().open_file(file_name)
            else:
                sublime.error_message("Aucun fichier n'a été sauvegardé sur cette position. Veuillez utiliser Win+Fx pour définir le fichier courant comme préféré.")


class PutInFileCommand(sublime_plugin.TextCommand):
    def run(self, edit, text=""):
        self.view.set_syntax_file('Packages/Diff/Diff.tmLanguage')
        text+="\n\n-!##############################################################################\n++++++++++++++++++++++++++++++++++++ Output ++++++++++++++++++++++++++++++++++++\n########### Utilisation avec \"Ctrl + <\" sur une des commandes en bas ###########\n------ (Execute) +++ (Check_status) +++ (Place_in_Project) +++ (Clear_Output)\n-0############################################################################0\n"
        self.view.insert(edit, 0, text)
        # self.view.set_read_only(True)
        self.view.set_scratch(True)



###
### GIT
###
# diff --git a/README b/README
class GitDiffFormatCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.set_read_only(False)
        sublime.status_message("Diff in pending...")
        contenu_total = sublime.Region(0, self.view.size())
        content = str(self.view.substr(contenu_total))
        # content = ''
        content = re.sub(r'diff\s--git\sa/([^\s]+)\s.*(?:\nnew\sfile.*)?\nindex.*\n.*\n.*', r'\n################################################################################\n>>>>>    \1\n################################################################################\n\n', content)
        # content = re.sub(r'diff\s--git\sa/([^\s]+)\s)b/[^\s]+', r'\n################################################################################\n--->    \2\n################################################################################\n\n\1', content)
        content = re.sub(r'(--->\s+)([^\s]+/)([^\s/]+)', r'\1\3    ::::    \2', content)
        # content+="\n\n\n+++++    Current Commit    +++++\n.ST_PROJECT git pull -u|!| 0 files unresolved,|,no changes found\n.ST_PROJECT git reset |!| "
        self.view.set_syntax_file('Packages/Diff/Diff.tmLanguage')
        self.view.replace(edit, contenu_total, content)
        # replace_all(self, "")
        # replace_all(self, content)


class GitAddCommitCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        contenu_total = sublime.Region(0, self.view.size())
        content = str(self.view.substr(contenu_total))
        selections = self.view.sel()
        check_right_line = re.compile("^--->\s+")
        coord_line = None
        ligne = None
        for selection in selections:
            coord_line = self.view.line(selection)
            ligne = self.view.substr(coord_line)
            if check_right_line.match(ligne):
                line_add = re.sub(r'(--->\s+)([^\s]+)\s*:+\s*([^\s]+)', r' \3\2', ligne)
                content += line_add
                content+="\n.ST_PROJECT git add "+line_add
        self.view.replace(edit, contenu_total, content)
        self.view.replace(edit, coord_line, ligne+"\n+ Current commit")
        sublime.status_message("Ajout effectué")


class GitCommitDiffCommand(sublime_plugin.TextCommand):
    def run(self, edit, message=None):
        if not message:
            self.view.window().show_input_panel("Message de Commit", "", self.on_done, self.on_change, self.on_cancel)
        else:
            contenu_total = sublime.Region(0, self.view.size())
            content = str(self.view.substr(contenu_total))
            content+=" -m \""+message+"\"\n.ST_PROJECT git log -v --limit 1 |!| "+message+"\nCheck status\n.ST_PROJECT git push origin master |!| Last revision is now"
            self.view.replace(edit, contenu_total, content)
    def on_done(self, choix):
        if len(choix)<5:
            sublime.error_message("Le message de commit doit être supérieur à 5 caractères")
            self.view.window().run_command('git_commit_diff')
        else:
            self.view.window().run_command('git_commit_diff', {"message": choix})

    def on_change(self, choix):
        print ("on_change")

    def on_cancel(self, choix):
        print ("on_cancel")


###
### MERCURIAL
###
class DiffFormatCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        contenu_total = sublime.Region(0, self.view.size())
        content = str(self.view.substr(contenu_total))
        content = "+ Utilisation : \nwin+h, win+a (curseur sur la ligne d'un fichier) ajoute au prochain commit\nwin+h, win+c : finalise le prochain commit\n"+content
        # content = re.sub(r'(diff\s\-r\s\w+\s([^\s]+))', r'\n################################################################################\n--->    \2\n################################################################################\n\n\1', content)
        content = re.sub(r'(diff\s\-r\s\w+(?:\s\-r\s\w+)?\s([^\s]+))', r'\n################################################################################\n--->    \2\n################################################################################\n\n\1', content)
        content = re.sub(r'(--->\s+)([^\s]+/)([^\s/]+)', r'\1\3    ::::    \2', content)
        content+="\n\n\n+++++    Current Commit    +++++\n.ST_PROJECT hg pull -u|!| 0 files unresolved,|,no changes found\n.ST_PROJECT hg branch\n.ST_PROJECT hg commit"
        self.view.replace(edit, contenu_total, content)



class AddCommitCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        contenu_total = sublime.Region(0, self.view.size())
        content = str(self.view.substr(contenu_total))
        selections = self.view.sel()
        check_right_line = re.compile("^--->\s+")
        coord_line = None
        ligne = None
        for selection in selections:
            coord_line = self.view.line(selection)
            ligne = self.view.substr(coord_line)
            if check_right_line.match(ligne):
                line_add = re.sub(r'(--->\s+)([^\s]+)\s*:+\s*([^\s]+)', r' \3\2', ligne)
                content += line_add
            else:
                line_add = re.sub(r'.\s([^\s]+)', r' \1', ligne)
                content += line_add
                # content+="\n"+line_add
                # self.view.replace(edit, coord_line, ligne+"\n+Current commit")
        self.view.replace(edit, contenu_total, content)
        self.view.replace(edit, coord_line, ligne+"\n+ Current commit")
        sublime.status_message("Ajout effectué")


class RevertDiffCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        contenu_total = sublime.Region(0, self.view.size())
        content = str(self.view.substr(contenu_total))
        selections = self.view.sel()
        check_right_line = re.compile("^--->\s+")
        check_orig = re.compile("^.\s.*orig$")
        coord_line = None
        ligne = None
        for selection in selections:
            coord_line = self.view.line(selection)
            ligne = self.view.substr(coord_line)
            if check_right_line.match(ligne):
                line_add = re.sub(r'(--->\s+)([^\s]+)\s*:+\s*([^\s]+)', r'.ST_PROJECT hg revert \3\2', ligne)
                content+="\n"+line_add
                # self.view.replace(edit, coord_line, ligne+"\n+Current commit")
            elif check_orig.match(ligne):
                line_add = re.sub(r'^.\s([^\s]+)$', r'.ST_PROJECT rm -f \1', ligne)
                content+="\n"+line_add
        self.view.replace(edit, contenu_total, content)
        self.view.replace(edit, coord_line, ligne+"\n-TO REVERT")
        sublime.status_message("Ajout effectué")


class CommitDiffCommand(sublime_plugin.TextCommand):
    def run(self, edit, message=None):
        if not message:
            self.view.window().show_input_panel("Message de Commit", "", self.on_done, self.on_change, self.on_cancel)
        else:
            contenu_total = sublime.Region(0, self.view.size())
            content = str(self.view.substr(contenu_total))
            content+=" -m \""+message+"\"\n.ST_PROJECT hg log -v --stat --limit 1 |!| "+message+"\nCheck status\n.ST_PROJECT hg push |!| Last revision is now"
            self.view.replace(edit, contenu_total, content)
    def on_done(self, choix):
        if len(choix)<5:
            sublime.error_message("Le message de commit doit être supérieur à 5 caractères")
            self.view.window().run_command('commit_diff')
        else:
            self.view.window().run_command('commit_diff', {"message": choix})

    def on_change(self, choix):
        print ("on_change")

    def on_cancel(self, choix):
        print ("on_cancel")


def replace_all(instance, content):
    all_content = sublime.Region(0, instance.view.size())
    instance.view.sel().add(all_content)
    selections = instance.view.sel()
    for selection in selections:
        text = str(instance.view.substr(selection))
        with Edit(instance.view) as edit:
            edit.replace(selection, content);






class Clock(object):

    CLOCK_ID = '00_clock'
    text = ''

    running = False

    @classmethod
    def start(cls):
        cls.running = True
        cls._tick()

    @classmethod
    def stop(cls):
        cls.running = False
        for window in sublime.windows():
            try:
                window.active_view().erase_status(cls.CLOCK_ID)
            except:
                pass

    @classmethod
    def paint(cls, view):
        view.set_status(cls.CLOCK_ID, cls.text)

    @classmethod
    def _tick(cls):
        try:
            if cls.running:
                sublime.set_timeout(cls._tick, cls._update())
        except Exception as error:
            print("Clock:", error)
            cls.stop()

    @classmethod
    def _update(cls):
        now = datetime.datetime.now()
        # The clock symbol displayes half and full hours.
        #
        # full hours:
        #   01:00 🕐 \U0001F550
        #   ...
        #   12:00 🕛 \U0001F55B
        #
        # half hours:
        #   01:30 🕜 \U0001F55C
        #   ...
        #   12:30 🕧 \U0001F567
        #
        # The 15 minutes offset causes the
        #  - half icons to be displayed between x:15 and x:45
        #  - full icons to be displayed between x:45 and x+1:15
        inow = now + datetime.timedelta(minutes=15)
        clock_icon = chr(0x1F550 + (inow.hour - 1) % 12 + 12 * (inow.minute >= 30))
        cal_icon = chr(0x1F4C5)
        cls.text = ' '.join((clock_icon, now.strftime('%H:%M'), cal_icon, now.strftime('%d.%m.%Y')))
        # update the clock of all windows
        for window in sublime.windows():
            try:
                cls.paint(window.active_view())
            except:
                pass
        return 1000 * (60 - now.second)


class EventListener(sublime_plugin.EventListener):
    def on_activated(self, view):
        """Redraw in case the view belongs to a new window."""
        Clock.paint(view)


def plugin_loaded():
    Clock.start()


def plugin_unloaded():
    Clock.stop()





# Classe qui sert à utiliser Edit() dans la méthode on_done
import sublime
import sublime_plugin
from collections import defaultdict
try:
    sublime.edit_storage
except AttributeError:
    sublime.edit_storage = {}
class EditStep:
    def __init__(self, cmd, *args):
        self.cmd = cmd
        self.args = args
    def run(self, view, edit):
        if self.cmd == 'callback':
            return self.args[0](view, edit)
        funcs = {
        'insert': view.insert,
        'erase': view.erase,
        'replace': view.replace,
        }
        func = funcs.get(self.cmd)
        if func:
            func(edit, *self.args)
class Edit:
    defer = defaultdict(dict)
    def __init__(self, view):
        self.view = view
        self.steps = []
    def step(self, cmd, *args):
        step = EditStep(cmd, *args)
        self.steps.append(step)
    def insert(self, point, string):
        self.step('insert', point, string)
    def erase(self, region):
        self.step('erase', region)
    def replace(self, region, string):
        self.step('replace', region, string)
    def callback(self, func):
        self.step('callback', func)
    def run(self, view, edit):
        for step in self.steps:
            step.run(view, edit)
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        view = self.view
        if sublime.version().startswith('2'):
            edit = view.begin_edit()
            self.run(edit)
            view.end_edit(edit)
        else:
            key = str(hash(tuple(self.steps)))
            sublime.edit_storage[key] = self.run
            view.run_command('apply_edit', {'key': key})
class apply_edit(sublime_plugin.TextCommand):
    def run(self, edit, key):
        sublime.edit_storage.pop(key)(self.view, edit)


