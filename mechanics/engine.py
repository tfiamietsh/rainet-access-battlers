from copy import deepcopy
from misc.constants import *
from misc import utils
import rainet


class Engine:
    @classmethod
    def make_move(cls, duel_info: DuelInfo, move, pl=P1):
        idx3 = None
        if len(move) == 3:
            idx1, idx2, idx3 = move
        else:
            idx1, idx2 = move
        phase, matrix, stack, skills = duel_info
        matrix, stack, skills = deepcopy(matrix), deepcopy(stack), deepcopy(skills)

        if idx1 in SKILL_INDICES.values() or idx2 in SKILL_INDICES.values():
            if pl == P1:
                rainet.RaiNet.play_sound(SKILL_SFX)
            if idx1 == SKILL_INDICES[LB]:
                matrix[idx2[0]][idx2[1]] += '+'
                skills[pl].remove(LB)
            elif idx2 == SKILL_INDICES[LB]:
                matrix[idx1[0]][idx1[1]] = utils.re_sub_plus(matrix[idx1[0]][idx1[1]])
                skills[pl].append(LB)
            elif idx1 == SKILL_INDICES[FW]:
                matrix[idx2[0]][idx2[1]] = FW + pl
                skills[pl].remove(FW)
            elif idx2 == SKILL_INDICES[FW]:
                matrix[idx1[0]][idx1[1]] = NC
                skills[pl].append(FW)
            elif idx1 == SKILL_INDICES[NF]:
                matrix[idx2[0]][idx2[1]], matrix[idx3[0]][idx3[1]] = \
                    utils.re_sub_minus(matrix[idx3[0]][idx3[1]]), utils.re_sub_minus(matrix[idx2[0]][idx2[1]])
                skills[pl].remove(NF)
            elif idx1 == SKILL_INDICES[VC]:
                matrix[idx2[0]][idx2[1]] += '-'
                skills[pl].remove(VC)
        else:
            if pl == P1:
                rainet.RaiNet.play_sound(ACTION_SFX)
            if matrix[idx2[0]][idx2[1]] == NC:
                matrix[idx1[0]][idx1[1]], matrix[idx2[0]][idx2[1]] = matrix[idx2[0]][idx2[1]], matrix[idx1[0]][idx1[1]]
                if phase == SETUP_PHASE:
                    n = {L1: 0, V1: 0, L2: 0, V2: 0}
                    indices = {
                        L1: P1_SERVER_PORTS[0], V1: P1_SERVER_PORTS[1],
                        L2: P2_SERVER_PORTS[1], V2: P2_SERVER_PORTS[0]
                    }
                    next_phase = True

                    for (i, j) in P1_SETUP_AREA + P2_SETUP_AREA:
                        if matrix[i][j] != NC:
                            n[matrix[i][j]] += 1
                    for key in n:
                        if n[key] < 4:
                            matrix[indices[key][0]][indices[key][1]] = key
                            next_phase = False
                    if next_phase:
                        phase = MAIN_CYCLE_PHASE
                        skills = {P1: [LB, FW, NF, VC], P2: [LB, FW, NF, VC]}
                elif phase == MAIN_CYCLE_PHASE:
                    for _pl, server_ports in [(P2, P1_SERVER_PORTS), (P1, P2_SERVER_PORTS)]:
                        if _pl in matrix[idx2[0]][idx2[1]] and idx2 in server_ports:
                            if '+' in matrix[idx2[0]][idx2[1]]:
                                skills[_pl] += LB
                            Engine._add_to_stack(stack, _pl, matrix[idx2[0]][idx2[1]])
                            matrix[idx2[0]][idx2[1]] = NC
                            break
            else:
                Engine._add_to_stack(stack, pl, matrix[idx2[0]][idx2[1]])
                if '+' in matrix[idx2[0]][idx2[1]]:
                    skills[P1 if pl == P2 else P2].append(LB)
                matrix[idx1[0]][idx1[1]], matrix[idx2[0]][idx2[1]] = NC, matrix[idx1[0]][idx1[1]]
        return DuelInfo(phase, matrix, stack, skills)

    @classmethod
    def get_valid_moves(cls, duel_info, pl=P1, include_skills=True):
        phase, matrix, _, skills = duel_info
        valid_moves = []

        if phase == SETUP_PHASE:
            all_indices, ports = (P1_SETUP_AREA, P1_SERVER_PORTS) if pl == P1 else (P2_SETUP_AREA, P2_SERVER_PORTS)
            nc_indices = [(i, j) for i, j in all_indices if matrix[i][j] == NC]

            for _from in P1_SERVER_PORTS:
                valid_moves += [[_from, _to] for _to in nc_indices]
            valid_moves += [[port, _to] for _to in nc_indices for port in ports]
        elif phase == MAIN_CYCLE_PHASE:
            def is_accessible_space(i, j):
                if pl == P1:
                    return 0 <= i <= 7 and 0 <= j <= 7 and (i, j) not in P1_SERVER_PORTS and \
                           (matrix[i][j] == NC or L2 in matrix[i][j] or V2 in matrix[i][j])
                else:
                    return 0 <= i <= 7 and 0 <= j <= 7 and (i, j) not in P2_SERVER_PORTS and \
                           (matrix[i][j] == NC or L1 in matrix[i][j] or V1 in matrix[i][j])

            all_indices = [(i, j) for j in range(8) for i in range(8)]
            pl_card_indices = [(i, j) for i, j in all_indices if pl in matrix[i][j] and FW not in matrix[i][j]]
            op = P1 if pl == P2 else P2
            op_card_indices = [(i, j) for i, j in all_indices if op in matrix[i][j] and FW not in matrix[i][j]]
            nc_indices = [(i, j) for i, j in all_indices if matrix[i][j] == NC]
            steps = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            fw_card_idx, lb_card_idx = None, None

            for i, j in all_indices:
                if pl in matrix[i][j]:
                    if FW in matrix[i][j]:
                        fw_card_idx = (i, j)
                    if '+' in matrix[i][j]:
                        lb_card_idx = (i, j)
            for i, j in pl_card_indices:
                for d_i, d_j in steps:
                    if is_accessible_space(i + d_i, j + d_j):
                        valid_moves.append([(i, j), (i + d_i, j + d_j)])
            if include_skills:
                if LB in skills[pl]:
                    for idx in pl_card_indices:
                        valid_moves.append([SKILL_INDICES[LB], idx])
                else:
                    if lb_card_idx is not None:
                        def check_and_append_lb_card_move(_d_i, _d_j):
                            if is_accessible_space(lb_card_idx[0] + _d_i, lb_card_idx[1] + _d_j) and \
                                    is_accessible_space(lb_card_idx[0] + 2 * _d_i, lb_card_idx[1] + 2 * _d_j):
                                valid_moves.append([lb_card_idx, (lb_card_idx[0] + 2 * _d_i, lb_card_idx[1] + 2 * _d_j)])

                        for d_i, d_j in steps:
                            check_and_append_lb_card_move(d_i, d_j)
                        valid_moves.append([lb_card_idx, SKILL_INDICES[LB]])
                if FW in skills[pl]:
                    for idx in nc_indices:
                        if idx not in P1_SERVER_PORTS + P2_SERVER_PORTS:
                            valid_moves.append([SKILL_INDICES[FW], idx])
                else:
                    if fw_card_idx is not None:
                        valid_moves.append([fw_card_idx, SKILL_INDICES[FW]])
                if NF in skills[pl]:
                    for idx1 in pl_card_indices:
                        for idx2 in pl_card_indices:
                            if idx1 != idx2:
                                valid_moves.append([SKILL_INDICES[NF], idx1, idx2])
                if VC in skills[pl]:
                    for idx in op_card_indices:
                        valid_moves.append([SKILL_INDICES[VC], idx])
        return valid_moves

    @classmethod
    def _add_to_stack(cls, stack, pl, card):
        stack[pl][LNKS if 'l' in card else VIRS].append(utils.re_sub_a_z(card))
