import streamlit as st
import random
from PIL import Image, ImageDraw

# Constants
BOARD_SIZE = 15  # 15x15 grid for Ludo
CELL_SIZE = 30
IMAGE_SIZE = BOARD_SIZE * CELL_SIZE

# Player colors and starting positions (one token per player for demo)
players = {
    "Red": {"color": (255, 0, 0), "start_pos": (1, 1)},
    "Green": {"color": (0, 255, 0), "start_pos": (1, 13)},
    "Yellow": {"color": (255, 255, 0), "start_pos": (13, 13)},
    "Blue": {"color": (0, 0, 255), "start_pos": (13, 1)}
}

# Simple path for demonstration (around the border cells clockwise)
path = [
    (1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9),(1,10),(1,11),(1,12),(1,13),
    (2,13),(3,13),(4,13),(5,13),(6,13),(7,13),(8,13),(9,13),(10,13),(11,13),(12,13),(13,13),
    (13,12),(13,11),(13,10),(13,9),(13,8),(13,7),(13,6),(13,5),(13,4),(13,3),(13,2),(13,1),
    (12,1),(11,1),(10,1),(9,1),(8,1),(7,1),(6,1),(5,1),(4,1),(3,1),(2,1)
]

def draw_board(player_positions):
    img = Image.new('RGB', (IMAGE_SIZE, IMAGE_SIZE), 'white')
    draw = ImageDraw.Draw(img)

    # Draw grid
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            x0, y0 = j*CELL_SIZE, i*CELL_SIZE
            x1, y1 = x0+CELL_SIZE, y0+CELL_SIZE

            # Fill starting corners with player colors
            if (i, j) == (1,1):
                draw.rectangle([x0, y0, x1, y1], fill=players["Red"]["color"])
            elif (i, j) == (1,13):
                draw.rectangle([x0, y0, x1, y1], fill=players["Green"]["color"])
            elif (i, j) == (13,13):
                draw.rectangle([x0, y0, x1, y1], fill=players["Yellow"]["color"])
            elif (i, j) == (13,1):
                draw.rectangle([x0, y0, x1, y1], fill=players["Blue"]["color"])
            else:
                draw.rectangle([x0, y0, x1, y1], outline='gray')

    # Draw players
    for player, pos_idx in player_positions.items():
        if pos_idx is not None and 0 <= pos_idx < len(path):
            y, x = path[pos_idx]
            cx = x * CELL_SIZE + CELL_SIZE//2
            cy = y * CELL_SIZE + CELL_SIZE//2
            r = CELL_SIZE//3
            draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=players[player]["color"])

    return img

# Initialize session state
if "player_positions" not in st.session_state:
    st.session_state.player_positions = {p: None for p in players}  # None means at start, not on path
if "current_player" not in st.session_state:
    st.session_state.current_player = "Red"
if "dice_roll" not in st.session_state:
    st.session_state.dice_roll = 0

st.title("🎲 Simple 4-Player Ludo (Demo)")

st.write(f"**Current Player:** {st.session_state.current_player}")
st.write(f"**Last Dice Roll:** {st.session_state.dice_roll}")

if st.button("Roll Dice 🎲"):
    roll = random.randint(1, 6)
    st.session_state.dice_roll = roll
    player = st.session_state.current_player
    pos = st.session_state.player_positions[player]

    # If player not started, only start moving if roll == 6
    if pos is None:
        if roll == 6:
            st.session_state.player_positions[player] = 0
            st.success(f"{player} entered the board!")
        else:
            st.info(f"{player} needs a 6 to enter the board.")
    else:
        # Move forward roll steps, looping path if needed
        new_pos = (pos + roll) % len(path)
        st.session_state.player_positions[player] = new_pos
        st.success(f"{player} moved {roll} steps.")

    # Switch turn unless roll was 6 (player gets extra turn)
    if roll != 6:
        players_list = list(players.keys())
        current_idx = players_list.index(player)
        next_idx = (current_idx + 1) % len(players_list)
        st.session_state.current_player = players_list[next_idx]

# Draw board with current positions
board_img = draw_board(st.session_state.player_positions)
st.image(board_img, width=IMAGE_SIZE)

st.write("**Legend:**")
for p in players:
    st.markdown(f"- <span style='color: rgb{players[p]['color']}; font-weight:bold;'>{p}</span>", unsafe_allow_html=True)
