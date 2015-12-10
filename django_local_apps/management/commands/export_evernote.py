import os

from django.contrib.auth.models import User

from django_local_apps.models import IndexedTime, IndexType
from django_local_apps.server_configurations import get_admin_username
from djangoautoconf.local_key_manager import get_local_key
from libtool import format_path
from obj_sys.models_ufs_obj import UfsObj
from obj_sys.obj_tools import get_ufs_url_for_local_path
from universal_clipboard.management.commands.cmd_handler_base.msg_process_cmd_base import MsgProcessCommandBase

# The following codes are modified from:
# https://github.com/evernote/evernote-sdk-python/blob/master/sample/client/EDAMTest.py

#
# A simple Evernote API demo script that lists all notebooks in the user's
# account and creates a simple test note in the default notebook.
#
# Before running this sample, you must fill in your Evernote developer token.
#
# To run (Unix):
#   export PYTHONPATH=../../lib; python EDAMTest.py
#

import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types

from evernote.api.client import EvernoteClient

# Work around for certification error from:
# http://stackoverflow.com/questions/27835619/ssl-certificate-verify-failed-error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# Codes from https://github.com/gabrielhpugliese/familybook/blob/master/familybook/evernote_facades.py
import evernote.edam.notestore.ttypes as NoteTypes


class ExportEvernoteCmd(MsgProcessCommandBase):
    """
    """
    def __init__(self):
        super(ExportEvernoteCmd, self).__init__()
        self.auth_token = get_local_key("evernote_key.auth_token", "django_local_apps")

    def msg_loop(self):
        # Real applications authenticate with Evernote using OAuth, but for the
        # purpose of exploring the API, you can get a developer token that allows
        # you to access your own Evernote account. To get a developer token, visit
        # https://sandbox.evernote.com/api/DeveloperToken.action

        if self.auth_token == "your developer token":
            print "Please fill in your developer token"
            print "To get a developer token, visit " \
                "https://sandbox.evernote.com/api/DeveloperToken.action"
            exit(1)

        # Initial development is performed on our sandbox server. To use the production
        # service, change sandbox=False and replace your
        # developer token above with a token from
        # https://www.evernote.com/api/DeveloperToken.action
        client = EvernoteClient(token=self.auth_token, sandbox=True)

        user_store = client.get_user_store()

        version_ok = user_store.checkVersion(
            "Evernote EDAMTest (Python)",
            UserStoreConstants.EDAM_VERSION_MAJOR,
            UserStoreConstants.EDAM_VERSION_MINOR
        )
        print "Is my Evernote API version up to date? ", str(version_ok)
        print ""
        if not version_ok:
            exit(1)

        note_store = client.get_note_store()

        # List all of the notebooks in the user's account
        notebooks = note_store.listNotebooks()
        print "Found ", len(notebooks), " notebooks:"
        for notebook in notebooks:
            print "  * ", notebook.name
            for note in self.list_notes(notebook.guid, user_store, note_store):
                print note

    def list_notes(self, notebook_guid, user_store, note_store):
        note_filter = NoteTypes.NoteFilter()
        note_filter.notebookGuid = notebook_guid
        notes = note_store.findNotes(self.auth_token,
                                     note_filter, 0, 100).notes
        notes_lst = []
        for note in notes:
            # this_note = {'NoteTitle': note.title, 'NoteId': note.guid}
            this_note = {'NoteGuid': note.guid, 'NoteContent': note.content}
            notes_lst.append(this_note)

        return notes_lst


        # print
        # print "Creating a new note in the default notebook"
        # print
        #
        # # To create a new note, simply create a new Note object and fill in
        # # attributes such as the note's title.
        # note = Types.Note()
        # note.title = "Test note from EDAMTest.py"
        #
        # # To include an attachment such as an image in a note, first create a Resource
        # # for the attachment. At a minimum, the Resource contains the binary attachment
        # # data, an MD5 hash of the binary data, and the attachment MIME type.
        # # It can also include attributes such as filename and location.
        # image = open('enlogo.png', 'rb').read()
        # md5 = hashlib.md5()
        # md5.update(image)
        # hash = md5.digest()
        #
        # data = Types.Data()
        # data.size = len(image)
        # data.bodyHash = hash
        # data.body = image
        #
        # resource = Types.Resource()
        # resource.mime = 'image/png'
        # resource.data = data
        #
        # # Now, add the new Resource to the note's list of resources
        # note.resources = [resource]
        #
        # # To display the Resource as part of the note's content, include an <en-media>
        # # tag in the note's ENML content. The en-media tag identifies the corresponding
        # # Resource using the MD5 hash.
        # hash_hex = binascii.hexlify(hash)
        #
        # # The content of an Evernote note is represented using Evernote Markup Language
        # # (ENML). The full ENML specification can be found in the Evernote API Overview
        # # at http://dev.evernote.com/documentation/cloud/chapters/ENML.php
        # note.content = '<?xml version="1.0" encoding="UTF-8"?>'
        # note.content += '<!DOCTYPE en-note SYSTEM ' \
        #     '"http://xml.evernote.com/pub/enml2.dtd">'
        # note.content += '<en-note>Here is the Evernote logo:<br/>'
        # note.content += '<en-media type="image/png" hash="' + hash_hex + '"/>'
        # note.content += '</en-note>'
        #
        # # Finally, send the new note to Evernote using the createNote method
        # # The new Note object that is returned will contain server-generated
        # # attributes such as the new note's unique GUID.
        # created_note = note_store.createNote(note)
        #
        # print "Successfully created a new note with GUID: ", created_note.guid


Command = ExportEvernoteCmd
