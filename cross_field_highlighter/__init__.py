from aqt import gui_hooks

from .common.collection_holder import CollectionHolder
from .ui.profile_did_open_hook import ProfileDidOpenHook

collection_holder: CollectionHolder = CollectionHolder()
profile_did_open: ProfileDidOpenHook = ProfileDidOpenHook(collection_holder)
gui_hooks.collection_did_load.append(lambda col: collection_holder.set_collection(col))
gui_hooks.profile_did_open.append(profile_did_open)
