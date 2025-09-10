import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ASSETS = lambda name: os.path.join(BASE_DIR, "assets", name)


PATHS = {
    "exit": ASSETS("invite/exit.png"),
    "continue_battlepass": ASSETS("invite/continue_battlepass.png"),
    "warzone": ASSETS("invite/warzone.png"),
    "battleroyale": ASSETS("invite/battleroyale_mode.png"),
    "resurgence": ASSETS("invite/resurgence_mode.png"),
    "quads": ASSETS("invite/quads.png"),
    "party_settings": ASSETS("party/party_settings.png"),
    "invite_only": ASSETS("party/invite_only.png"),
    "add_friends": ASSETS("invite/add_friends.png"),
    "input": ASSETS("invite/input.png"),
    "send_request": ASSETS("invite/sendrequest.png"),
    "request_sent": ASSETS("invite/sent.png"),
    "back_button": ASSETS("back_button.png"),
    "failed_send":ASSETS("invite/failedsend.png"),
    "search_players": ASSETS("friends/searchplayers.png"),
    "not_found": ASSETS("friends/not_found.png"),
    "player_select": ASSETS("party/player_select.png"),
    "invite_party": ASSETS("party/invite_party.png"),
    "joined_party": ASSETS("party/joined_party.png"),
    "invite_accept": ASSETS("party/invite_accept.png"),
    "queue": ASSETS("game/queue.png"),
    "loadouts": ASSETS("game/loadouts.png"),
    "leave": ASSETS("game/leave.png"),
    "leave_confirm": ASSETS("game/leave_confirm.png"),
    "leave_confirm_notleader": ASSETS("game/leave_confirm_notleader.png"),
    "searching":  ASSETS("game/searching.png"),
    "cancel_search":  ASSETS("game/cancel_search.png"),
    "confirm_cancel_search":  ASSETS("game/confirm_cancel_search.png")
}

