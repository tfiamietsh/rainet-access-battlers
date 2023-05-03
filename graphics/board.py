from misc.constants import *
from misc import utils
from graphics.cards import Card
import rainet


class Board:
    @classmethod
    def draw(cls, styles, duel_info, lookup_idx):
        _, board, stack, skills = duel_info
        half_field_size = (FIELD_SIZE[0], FIELD_SIZE[1] // 2)

        rainet.RaiNet.screen.blit(rainet.RaiNet.img, (0, FIELD_SIZE[1] // 2), (*FIELD_OFFSETS, *half_field_size))
        rainet.RaiNet.screen.blit(rainet.RaiNet.inv_img, (0, 0),
                                  (*utils.inverted(half_field_size, FIELD_OFFSETS), *half_field_size))
        rainet.RaiNet.screen.blit(rainet.RaiNet.img, FIELD_STYLE_1_OFFSETS,
                                  (*FIELD_STYLES_OFFSETS[styles[0]], *FIELD_STYLE_SIZE))
        rainet.RaiNet.screen.blit(rainet.RaiNet.inv_img, FIELD_STYLE_2_OFFSETS,
                                  (*utils.inverted(FIELD_STYLE_SIZE, FIELD_STYLES_OFFSETS[styles[1]]),
                                   *FIELD_STYLE_SIZE))
        rainet.RaiNet.screen.blit(rainet.RaiNet.img, (0, FIELD_SIZE[1] // 2), (*SKILLS_OFFSETS, *half_field_size))

        def stack_indices(_i, _pl, _card_type):
            return 9.35 if _pl == P1 else -2.35, 7.75 - _i \
                if (_pl, _card_type) in [(P1, LNKS), (P2, VIRS)] else _i - .75

        def card_type(_card, idx):
            return ('l' if 'l' in _card else 'v') if (i, j) == idx or '-' in _card else 'h'

        for pl in [P1, P2]:
            for _card_type in [LNKS, VIRS]:
                for i, card in enumerate(stack[pl][_card_type]):
                    Card.draw(card_type=_card_type[0], card_style=styles[0] if P1 in card else styles[1],
                              card_pos=utils.indices_to_pos(stack_indices(i, pl, _card_type)), is_inverted=pl == P2)
        for i, line in enumerate(board):
            for j, card in enumerate(line):
                if card != NC:
                    if L1 in card or V1 in card:
                        Card.draw(card_type=card_type(card, lookup_idx), card_style=styles[0],
                                  card_pos=utils.indices_to_pos((i, j)))
                    elif L2 in card or V2 in card:
                        Card.draw(card_type=card_type(card, None), card_style=styles[1],
                                  card_pos=utils.indices_to_pos((i, j)), is_inverted=True)
                    elif FW in card:
                        Card.draw(card_type='f', card_pos=utils.indices_to_pos((i, j)), card_style=None)
                    if '+' in card:
                        Card.draw(card_type='+', card_pos=utils.indices_to_pos((i, j)), card_style=None)
        for skill in skills[P1]:
            Card.draw(card_type=skill, card_style=styles[0], card_pos=P1_SKILL_POS[skill])
