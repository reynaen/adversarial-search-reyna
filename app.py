"""
RPSLS Adversarial Search — Flask Backend
Kecerdasan Buatan | S1 Teknik Informatika

Implements:
  - Minimax Algorithm (pure)
  - Alpha-Beta Pruning (optimized Minimax)
  - Game Tree Builder (for visualization, max 3 levels)
  - REST API endpoints

RPSLS is a simultaneous-move zero-sum game:
  - AI (MAX player) picks a move aiming to MAXIMIZE score
  - Human (MIN player) responds, aiming to MINIMIZE score
  - Evaluation: +1 AI wins, -1 Human wins, 0 Draw
"""

from flask import Flask, render_template, request, jsonify
import time
import math
import random
import random

app = Flask(__name__)

# ─────────────────────────────────────────────
# GAME CONSTANTS
# ─────────────────────────────────────────────

MOVES = ['rock', 'paper', 'scissors', 'lizard', 'spock']

EMOJI = {
    'rock': '🪨', 'paper': '📄',
    'scissors': '✂️', 'lizard': '🦎', 'spock': '🖖'
}

# wins[a] → list of moves that 'a' defeats
WINS = {
    'rock':     ['scissors', 'lizard'],
    'paper':    ['rock',     'spock'],
    'scissors': ['paper',    'lizard'],
    'lizard':   ['paper',    'spock'],
    'spock':    ['rock',     'scissors'],
}

WIN_MESSAGES = {
    ('rock',     'scissors'): 'Rock crushes Scissors',
    ('rock',     'lizard'):   'Rock crushes Lizard',
    ('paper',    'rock'):     'Paper covers Rock',
    ('paper',    'spock'):    'Paper disproves Spock',
    ('scissors', 'paper'):    'Scissors cuts Paper',
    ('scissors', 'lizard'):   'Scissors cuts Lizard',
    ('lizard',   'paper'):    'Lizard eats Paper',
    ('lizard',   'spock'):    'Lizard poisons Spock',
    ('spock',    'rock'):     'Spock vaporizes Rock',
    ('spock',    'scissors'): 'Spock smashes Scissors',
}


def outcome(a: str, b: str) -> int:
    """
    Returns result from AI (a) perspective:
      +1  → AI wins
      -1  → Human wins
       0  → Draw
    """
    if a == b:
        return 0
    return 1 if b in WINS[a] else -1


# ─────────────────────────────────────────────
# MINIMAX — Pure (no pruning)
#
# Tree structure for RPSLS (simultaneous game):
#   Root → MAX level (AI chooses ai_move)
#         → MIN level (Human chooses human_move)
#               → Terminal: evaluate outcome(ai_move, human_move)
#
# counter[0] accumulates nodes visited across all branches.
# ─────────────────────────────────────────────

def minimax(depth: int, counter: list) -> tuple[int, str]:
    """
    Full Minimax search from root.
    Returns (best_value, best_ai_move).
    Randomly breaks ties among equally-valued moves.
    """
    counter[0] += 1  # root node

    best_val   = -math.inf
    best_moves = []

    for ai_move in MOVES:
        move_val = _minimax_min(ai_move, depth - 1, counter)
        if move_val > best_val:
            best_val   = move_val
            best_moves = [ai_move]
        elif move_val == best_val:
            best_moves.append(ai_move)

    return best_val, random.choice(best_moves)


def _minimax_min(ai_move: str, depth: int, counter: list) -> int:
    """Human (MIN) picks the worst response for AI."""
    counter[0] += 1

    if depth == 0:
        # Evaluate all human responses directly
        worst = math.inf
        for human_move in MOVES:
            counter[0] += 1
            val = outcome(ai_move, human_move)
            if val < worst:
                worst = val
        return worst

    # Deeper game tree: human picks, then AI picks again
    worst = math.inf
    for human_move in MOVES:
        val = _minimax_max(depth - 1, counter)
        if val < worst:
            worst = val
    return worst


def _minimax_max(depth: int, counter: list) -> int:
    """AI (MAX) picks best move at a deeper level."""
    counter[0] += 1

    if depth == 0:
        return 0  # neutral at max depth

    best = -math.inf
    for ai_move in MOVES:
        val = _minimax_min(ai_move, depth - 1, counter)
        if val > best:
            best = val
    return best


# ─────────────────────────────────────────────
# ALPHA-BETA PRUNING
#
# Same tree as Minimax, but:
#   α = best score MAX (AI) can guarantee  → prune when β ≤ α (at MIN level)
#   β = best score MIN (Human) can guarantee → prune when β ≤ α (at MAX level)
# ─────────────────────────────────────────────

def alpha_beta(depth: int, counter: list) -> tuple[int, str]:
    """
    Full Alpha-Beta search from root.
    Returns (best_value, best_ai_move).
    Randomly breaks ties among equally-valued moves.
    """
    counter[0] += 1  # root node

    best_val   = -math.inf
    best_moves = []
    alpha      = -math.inf
    beta       =  math.inf

    for ai_move in MOVES:
        move_val = _ab_min(ai_move, depth - 1, alpha, beta, counter)
        if move_val > best_val:
            best_val   = move_val
            best_moves = [ai_move]
        elif move_val == best_val:
            best_moves.append(ai_move)
        alpha = max(alpha, best_val)

    return best_val, random.choice(best_moves)


def _ab_min(ai_move: str, depth: int, alpha: float, beta: float, counter: list) -> int:
    """Human (MIN) — prune when β ≤ α."""
    counter[0] += 1

    if depth == 0:
        worst = math.inf
        for human_move in MOVES:
            counter[0] += 1
            val = outcome(ai_move, human_move)
            if val < worst:
                worst = val
                beta = min(beta, worst)
            if beta <= alpha:          # α cut-off
                break
        return worst if worst != math.inf else 0

    worst = math.inf
    for human_move in MOVES:
        val = _ab_max(depth - 1, alpha, beta, counter)
        if val < worst:
            worst = val
            beta = min(beta, worst)
        if beta <= alpha:              # α cut-off
            break
    return worst if worst != math.inf else 0


def _ab_max(depth: int, alpha: float, beta: float, counter: list) -> int:
    """AI (MAX) — prune when β ≤ α."""
    counter[0] += 1

    if depth == 0:
        return 0

    best = -math.inf
    for ai_move in MOVES:
        val = _ab_min(ai_move, depth - 1, alpha, beta, counter)
        if val > best:
            best = val
            alpha = max(alpha, best)
        if beta <= alpha:              # β cut-off
            break
    return best if best != -math.inf else 0


# ─────────────────────────────────────────────
# BEST MOVE SELECTOR
# ─────────────────────────────────────────────

def get_best_move(depth: int, use_ab: bool) -> dict:
    """
    Runs both Minimax and Alpha-Beta, returns the chosen move
    along with comparison stats.
    """
    start = time.perf_counter()

    mm_counter = [0]
    _, best_mm = minimax(depth, mm_counter)

    ab_counter = [0]
    _, best_ab = alpha_beta(depth, ab_counter)

    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

    mm_nodes   = mm_counter[0]
    ab_nodes   = ab_counter[0]
    pruned     = mm_nodes - ab_nodes
    efficiency = round((pruned / mm_nodes * 100), 1) if mm_nodes > 0 else 0
    # AI picks randomly (RPSLS is symmetric — all moves equally optimal)
    chosen = random.choice(MOVES)

    return {
        'best_move':  chosen,
        'emoji':      EMOJI[chosen],
        'mm_nodes':   mm_nodes,
        'ab_nodes':   ab_nodes,
        'pruned':     pruned,
        'efficiency': efficiency,
        'elapsed_ms': elapsed_ms,
    }


# ─────────────────────────────────────────────
# GAME TREE BUILDER (for canvas visualization)
# Max 3 visible levels regardless of actual depth
# ─────────────────────────────────────────────

_nid = 0

def build_tree(depth: int, use_ab: bool) -> dict:
    """Build a JSON-serialisable tree for frontend canvas."""
    global _nid
    _nid = 0
    return _tree_max(depth, -math.inf, math.inf, use_ab)


def _tree_max(depth: int, alpha: float, beta: float, use_ab: bool) -> dict:
    global _nid
    node = {
        'id': _nid, 'is_max': True, 'ai_move': None, 'human_move': None,
        'value': None, 'pruned': False, 'children': []
    }
    _nid += 1

    if depth == 0:
        node['value'] = 0
        return node

    best = -math.inf
    a = alpha

    for i, ai_move in enumerate(MOVES):
        child = _tree_min(ai_move, depth - 1, a, beta, use_ab)
        node['children'].append(child)
        if child['value'] is not None and child['value'] > best:
            best = child['value']
            a = max(a, best)
        # No MAX-level beta cutoff needed at root

    node['value'] = best if best != -math.inf else 0
    return node


def _tree_min(ai_move: str, depth: int, alpha: float, beta: float, use_ab: bool) -> dict:
    global _nid
    node = {
        'id': _nid, 'is_max': False, 'ai_move': ai_move, 'human_move': None,
        'value': None, 'pruned': False, 'children': []
    }
    _nid += 1

    b = beta
    worst = math.inf

    for i, human_move in enumerate(MOVES):
        val = outcome(ai_move, human_move)

        if depth == 0:
            # Leaf node
            leaf = {
                'id': _nid, 'is_max': None, 'ai_move': ai_move, 'human_move': human_move,
                'value': val, 'pruned': False, 'children': []
            }
            _nid += 1
            node['children'].append(leaf)
            if val < worst:
                worst = val
                b = min(b, worst)
            if use_ab and b <= alpha:
                # Mark remaining as pruned
                for rem in MOVES[i + 1:]:
                    node['children'].append({
                        'id': _nid, 'pruned': True,
                        'ai_move': ai_move, 'human_move': rem,
                        'label': rem, 'emoji': EMOJI[rem], 'children': []
                    })
                    _nid += 1
                break
        else:
            child = _tree_max(depth - 1, alpha, b, use_ab)
            child['ai_move'] = ai_move
            child['human_move'] = human_move
            node['children'].append(child)
            if child['value'] is not None and child['value'] < worst:
                worst = child['value']
                b = min(b, worst)
            if use_ab and b <= alpha:
                for rem in MOVES[i + 1:]:
                    node['children'].append({
                        'id': _nid, 'pruned': True,
                        'label': rem, 'emoji': EMOJI[rem], 'children': []
                    })
                    _nid += 1
                break

    node['value'] = worst if worst != math.inf else 0
    return node


# ─────────────────────────────────────────────
# FLASK ROUTES
# ─────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/move', methods=['POST'])
def api_move():
    """POST { depth, use_ab } → best move + node stats"""
    data   = request.get_json()
    depth  = max(1, min(5, int(data.get('depth', 3))))
    use_ab = bool(data.get('use_ab', True))
    return jsonify(get_best_move(depth, use_ab))


@app.route('/api/tree', methods=['POST'])
def api_tree():
    """POST { depth, use_ab } → game tree JSON (max 2 levels for viz)"""
    global _nid
    _nid = 0
    data   = request.get_json()
    depth  = max(1, min(2, int(data.get('depth', 2))))
    use_ab = bool(data.get('use_ab', True))
    tree   = build_tree(depth, use_ab)
    return jsonify(tree)


@app.route('/api/outcome', methods=['POST'])
def api_outcome():
    """POST { human, ai } → result + message"""
    data     = request.get_json()
    human_mv = data.get('human')
    ai_mv    = data.get('ai')

    if human_mv not in MOVES or ai_mv not in MOVES:
        return jsonify({'error': 'Invalid move'}), 400

    res = outcome(ai_mv, human_mv)   # +1 = AI wins

    if res == 1:
        reason = WIN_MESSAGES.get((ai_mv, human_mv), '')
        msg    = f'🤖 AI Menang! {reason}'
        label  = 'ai'
    elif res == -1:
        reason = WIN_MESSAGES.get((human_mv, ai_mv), '')
        msg    = f'🏆 Anda Menang! {reason}'
        label  = 'human'
    else:
        msg   = f'🤝 Seri! Keduanya memilih {EMOJI[human_mv]}'
        label = 'draw'

    return jsonify({
        'result':    res,
        'message':   msg,
        'label':     label,
        'human_emoji': EMOJI[human_mv],
        'ai_emoji':    EMOJI[ai_mv],
    })


@app.route('/api/rules')
def api_rules():
    return jsonify([
        {'winner': w, 'winner_emoji': EMOJI[w], 'loser': l, 'loser_emoji': EMOJI[l]}
        for w, losers in WINS.items() for l in losers
    ])


if __name__ == '__main__':
    app.run(debug=True)