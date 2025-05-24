import streamlit as st
import random
import time

# Game configuration
GRID_SIZE = 10
SNAKE_COLOR = "green"
FOOD_COLOR = "red"
EMPTY_COLOR = "white"
UPDATE_DELAY = 0.2  # Seconds

# Initialize session state
if "snake" not in st.session_state:
    st.session_state.snake = [(5, 5)]
    st.session_state.food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    st.session_state.direction = "RIGHT"
    st.session_state.game_over = False

# Functions
def move_snake():
    if st.session_state.game_over:
        return

    head_x, head_y = st.session_state.snake[-1]
    dx, dy = {
        "UP": (-1, 0),
        "DOWN": (1, 0),
        "LEFT": (0, -1),
        "RIGHT": (0, 1)
    }[st.session_state.direction]

    new_head = (head_x + dx, head_y + dy)

    # Collision detection
    if (new_head in st.session_state.snake or
        not (0 <= new_head[0] < GRID_SIZE) or
        not (0 <= new_head[1] < GRID_SIZE)):
        st.session_state.game_over = True
        return

    st.session_state.snake.append(new_head)

    if new_head == st.session_state.food:
        while True:
            new_food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            if new_food not in st.session_state.snake:
                break
        st.session_state.food = new_food
    else:
        st.session_state.snake.pop(0)

def draw_board():
    board = ""
    for i in range(GRID_SIZE):
        row = ""
        for j in range(GRID_SIZE):
            if (i, j) in st.session_state.snake:
                row += f":{SNAKE_COLOR}_square:"
            elif (i, j) == st.session_state.food:
                row += f":{FOOD_COLOR}_square:"
            else:
                row += f":{EMPTY_COLOR}_square:"
        board += row + "\n"
    st.markdown(board)

def change_direction(new_direction):
    # Prevent snake from going directly opposite
    opposite = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
    if new_direction != opposite.get(st.session_state.direction):
        st.session_state.direction = new_direction
        move_snake()

# UI
st.title("🐍 Streamlit Snake Game")

if st.session_state.game_over:
    st.error("Game Over! Refresh to restart.")
else:
    col1, col2, col3 = st.columns(3)
    with col2:
        st.button("⬆️", on_click=lambda: change_direction("UP"))
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("⬅️", on_click=lambda: change_direction("LEFT"))
    with col2:
        st.button("⬇️", on_click=lambda: change_direction("DOWN"))
    with col3:
        st.button("➡️", on_click=lambda: change_direction("RIGHT"))

    draw_board()
