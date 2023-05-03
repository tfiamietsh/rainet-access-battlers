import rainet
from graphics import animation
from misc.constants import *
from misc import utils


class Card:
    _firewall = animation.AnimatedImage(rainet.RaiNet.img.subsurface(FIREWALL_RECT),
                                        frame_indices=FIREWALL_FRAME_INDICES, delay_ms=90)
    _lineboost = animation.AnimatedImage(rainet.RaiNet.img.subsurface(LINEBOOST_RECT),
                                         frame_indices=LINEBOOST_FRAME_INDICES, delay_ms=120)

    @classmethod
    def draw(cls, card_type, card_style, card_pos, is_inverted=False):
        if card_type == 'f':
            Card._firewall.draw((card_pos[0], card_pos[1] - 26))
        elif card_type == '+':
            Card._lineboost.draw(card_pos)
        else:
            if is_inverted:
                rainet.RaiNet.screen.blit(rainet.RaiNet.inv_img, card_pos,
                                          (*utils.inverted(CARD_SIZE, CARD_STYLES_OFFSETS[card_type][card_style]),
                                           *CARD_SIZE))
            else:
                rainet.RaiNet.screen.blit(rainet.RaiNet.img, card_pos, (*CARD_STYLES_OFFSETS[card_type][card_style],
                                                                        *CARD_SIZE))
