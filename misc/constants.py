from collections import namedtuple

IMAGE_SIZE = [2656, 1101]
BGI_OFFSETS = [1840, 0]
FIELD_SIZE = [816, 894]
FIELD_OFFSETS = [512, 447]
FIELD_STYLE_SIZE = [512, 208]
FIELD_STYLE_1_OFFSETS = [152, 585]
FIELD_STYLE_2_OFFSETS = [152, 101]
FIELD_STYLES_OFFSETS = [
    [664, 585],
    [1328, 447],
    [1328, 655],
    [1328, 863],
    [0, 447],
    [0, 655],
    [0, 863]
]
FIELD_START_POS = [152, 171]
CARD_SIZE = [64, 69]
CARD_STYLES_OFFSETS = {
    'l': [[576, 894], [576, 963], [576, 1032], [964, 894], [964, 963], [964, 1032], [1632, 69]],
    'v': [[640, 894], [640, 963], [640, 1032], [1028, 894], [1028, 963], [1028, 1032], [1632, 138]],
    'fw': [[708, 894], [708, 963], [708, 1032], [1096, 894], [1096, 963], [1096, 1032], [1632, 207]],
    'lb': [[512, 894], [512, 963], [512, 1032], [900, 894], [900, 963], [900, 1032], [1632, 0]],
    'vc': [[772, 894], [772, 963], [772, 1032], [1160, 894], [1160, 963], [1160, 1032], [1632, 276]],
    'nf': [[836, 894], [836, 963], [836, 1032], [1224, 894], [1224, 963], [1224, 1032], [1632, 345]],
    'h': [[1696, 0], [1696, 69], [1696, 138], [1696, 207], [1696, 276], [1696, 345], [1760, 0]]
}
NUM_STYLES = 7
CARD_INIT_POS = [346, 654]
OPPONENT_IMAGE_SIZE = [200, 120]
OPPONENT_OFFSETS = [
    [0, 0],
    [200, 0],
    [0, 120],
    [200, 120],
    [0, 240],
    [200, 240],
    [400, 0]
]
NUM_OPPONENTS = 7
NC = 'xx'
L1, V1 = 'l1', 'v1'
L2, V2 = 'l2', 'v2'
FW, LB, NF, VC = 'fw', 'lb', 'nf', 'vc'
P1, P2 = '1', '2'
LNKS, VIRS = 'links', 'viruses'
SETUP_PHASE, MAIN_CYCLE_PHASE = 0, 1
P1_SETUP_AREA = [(7, 0), (7, 1), (7, 2), (6, 3), (6, 4), (7, 5), (7, 6), (7, 7)]
P2_SETUP_AREA = [(0, 0), (0, 1), (0, 2), (1, 3), (1, 4), (0, 5), (0, 6), (0, 7)]
P1_SERVER_PORTS = [(7, 3), (7, 4)]
P2_SERVER_PORTS = [(0, 3), (0, 4)]
MAIN_MENU = 0
ROLE_SELECTION = 1
NEW_DUEL = 2
CONNECTION_ERROR = 3
JOIN_DUEL = 4
CONNECTION_CANNNOT = 5
STYLE_SELECTION = 6
CONNECTION_LOST = 7
DUEL = 8
DUEL_END = 9
OPTIONS = 10
ACTION_SFX = 'action'
DUEL_END_SFX = 'duel_end'
SKILL_SFX = 'skill'
FRAMES_PER_SECOND = 10
FIREWALL_RECT = (600, 64, 64, 360)
FIREWALL_FRAME_INDICES = [(0, 0), (1, 0), (2, 0), (3, 0)]
LINEBOOST_RECT = (664, 0, 128, 276)
LINEBOOST_FRAME_INDICES = [(0, 0), (0, 1), (1, 1), (2, 1), (3, 1), (1, 0), (2, 0), (3, 0)]
SPINNER_RECT = (1840, 894, 520, 64)
SPINNER_FRAME_INDICES = [(0, i) for i in range(8)]
SKILLS_OFFSETS = [816, 0]
P1_SKILL_POS = {
    'lb': [736, 619],
    'fw': [736, 757],
    'nf': [16, 619],
    'vc': [16, 757]
}
SKILL_INDICES = {
    'lb': (101, 101),
    'fw': (101, -101),
    'nf': (-101, 101),
    'vc': (-101, -101)
}
PLUG_IDX = (99, 99)
SECRET_KEY = 'mz275349O'

DuelInfo = namedtuple('DuelInfo', 'phase matrix stack skills')
