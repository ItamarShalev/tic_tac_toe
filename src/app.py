import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent / 'src'))

from flask import Flask, render_template, request, redirect, url_for
from src.game import Game
from src.data.exceptions import GameOver, InvalidMove

app = Flask(__name__)
games: dict[str, Game] = {}

def client_ip() -> str:
    return request.remote_addr or ""

@app.route('/')
def index():
    game = games.setdefault(client_ip(), Game())
    rendered_template = render_template(
        'index.html',
        board=game.board(),
        current_player=str(game.current_player),
        winner=game.state.value if game.state.game_over() else None
    )
    return rendered_template

@app.route('/move/<int:cell>')
def move(cell: int):
    game = games.setdefault(client_ip(), Game())
    try:
        game.play(cell)
    except (GameOver, InvalidMove):
        pass
    return redirect(url_for('index'))


@app.route('/reset')
def reset():
    games[client_ip()] = Game()
    return redirect(url_for('index'))


def main():
    port = int(os.environ.get('GAME_PORT', 80))
    app.run(port=port)

if __name__ == '__main__':
    main()
