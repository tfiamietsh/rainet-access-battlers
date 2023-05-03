import pygame
from misc.constants import *
from mechanics import engine
from graphics import board, ui, cards
from misc import utils
from network import bt
from functools import partial


class Duel:
    def __init__(self, p1_style, p2_style, connection, on_duel_end, on_connection_lost):
        font = ui.Font(40)

        self._styles = [p1_style, p2_style]
        self._duel_info = DuelInfo(
            phase=SETUP_PHASE,
            matrix=[
                [NC, NC, NC, V2, L2, NC, NC, NC],
                [NC, NC, NC, NC, NC, NC, NC, NC],
                [NC, NC, NC, NC, NC, NC, NC, NC],
                [NC, NC, NC, NC, NC, NC, NC, NC],
                [NC, NC, NC, NC, NC, NC, NC, NC],
                [NC, NC, NC, NC, NC, NC, NC, NC],
                [NC, NC, NC, NC, NC, NC, NC, NC],
                [NC, NC, NC, L1, V1, NC, NC, NC],
            ],
            stack={
                P1: {LNKS: [], VIRS: []},
                P2: {LNKS: [], VIRS: []}
            },
            skills={P1: [], P2: []})
        self._lookup_idx = None
        self._prev_indices = []
        self._history = []
        self._on_duel_end = on_duel_end
        self._on_connection_lost = on_connection_lost
        self._connection = connection
        self._player = P1 if isinstance(self._connection, bt.Server) else P2
        self._player_in_turn = P1
        self._labels = [ui.Label(font, 'You:', (20, 20)), ui.Label(font, 'Turn:', (730, 20)),
                        ui.Label(font, 'P' + self._player, (30, 60)),
                        ui.Label(font, 'P' + self._player_in_turn, (750, 60))]
        self._is_synchronized = self._player_in_turn == self._player

        if self._connection is not None and not self._is_synchronized and self._player != self._player_in_turn:
            utils.start_daemon_thread(self._sync)

    def update(self):
        board.Board.draw(self._styles, self._duel_info, self._lookup_idx)
        self._labels[-1].set_text('P' + self._player_in_turn)
        for label in self._labels:
            label.update()
        if self._connection is not None and not self._is_synchronized and self._player != self._player_in_turn:
            utils.start_daemon_thread(self._sync)
        self._hide_p2_server_cards_in_setup()

    def on_mouse_btn_up(self):
        if self._player == self._player_in_turn:
            mouse_pos = pygame.mouse.get_pos()
            i, j = utils.pos_to_indices(mouse_pos)
            for skill in [LB, FW, NF, VC]:
                if utils.is_pos_in_rect(mouse_pos, (*P1_SKILL_POS[skill], *CARD_SIZE)):
                    i, j = SKILL_INDICES[skill]
            self._prev_indices.append((i, j))
            n = len(self._prev_indices)

            if n > 1:
                valid_moves = engine.Engine.get_valid_moves(self._duel_info)
                if n > 2 and self._prev_indices[-3] == SKILL_INDICES[NF]:
                    move = [self._prev_indices[-3], self._prev_indices[-2], self._prev_indices[-1]]
                else:
                    move = [self._prev_indices[-2], self._prev_indices[-1]]

                if move in valid_moves:
                    self._duel_info = engine.Engine.make_move(self._duel_info, move, P1)
                    transformed_move = []

                    for pair in move:
                        if pair not in SKILL_INDICES.values():
                            transformed_move.append((7 - pair[0], 7 - pair[1]))
                        else:
                            transformed_move.append(pair)

                    def p1_make_move():
                        self._player_in_turn = {P1: P2, P2: P1}[self._player_in_turn]
                        if self._is_duel_end():
                            return
                        self._prev_indices.append(PLUG_IDX)

                    utils.try_else(partial(self._connection.send, data=str(transformed_move)),
                                   self._on_connection_lost, p1_make_move)
                    self._is_synchronized = False
            elif n > 3:
                self._prev_indices.remove(self._prev_indices[0])

    def on_mouse_move(self):
        self._lookup_idx = utils.pos_to_indices(pygame.mouse.get_pos())

    def _sync(self):
        self._is_synchronized = True

        def get_p2_move():
            return utils.str_to_pair_list(self._connection.recv())

        def if_disconnected():
            self._connection = None
            self._on_connection_lost()

        move = utils.try_else(get_p2_move, if_disconnected)

        if not isinstance(move, Exception):
            self._duel_info = engine.Engine.make_move(duel_info=self._duel_info, move=move, pl=P2)
            self._player_in_turn = {P1: P2, P2: P1}[self._player_in_turn]
            self._is_duel_end()

    def _is_duel_end(self):
        p1_num_links = len(self._duel_info.stack[P1][LNKS])
        p1_num_viruses = len(self._duel_info.stack[P1][VIRS])
        p2_num_links = len(self._duel_info.stack[P2][LNKS])
        p2_num_viruses = len(self._duel_info.stack[P2][VIRS])
        duel_end = False

        if p1_num_links == 4 or p2_num_viruses == 4:
            self._on_duel_end(P1)
            duel_end = True
        if p2_num_links == 4 or p1_num_viruses == 4:
            self._on_duel_end(P2)
            duel_end = True
        return duel_end

    def _hide_p2_server_cards_in_setup(self):
        if self._duel_info.phase == SETUP_PHASE:
            for idx in P2_SERVER_PORTS:
                cards.Card.draw(card_type='h', card_style=self._styles[1], card_pos=utils.indices_to_pos(idx))
