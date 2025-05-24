import streamlit as st
import time
from PIL import Image, ImageDraw
import random

# Constants
GRID_SIZE = 20
CELL_SIZE = 20
IMAGE_SIZE = GRID_SIZE * CELL_SIZE
SPEED_MAP = {"Easy": 0.3, "Medium": 0.15, "Hard": 0.08}

def draw_board(snake, food):
    img = Image.new('RGB', (IMAGE_SIZE, IMAGE_SIZE), color=(0, 128, 0))
    draw = ImageDraw.Draw(img)

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x0 = j * CELL_SIZE
            y0 = i * CELL_SIZE
            x1 = x0 + CELL_SIZE - 1
            y1 = y0 + CELL_SIZE - 1
            draw.rectangle([x0, y0, x1, y1], outline=(0, 100, 0))

    for y, x in snake:
        x0 = x * CELL_SIZE
        y0 = y * CELL_SIZE
        x1 = x0 + CELL_SIZE - 1
        y1 = y0 + CELL_SIZE - 1
        draw.rectangle([x0, y0, x1, y1], fill=(0, 0, 0))

    fy, fx = food
    x0 = fx * CELL_SIZE
    y0 = fy * CELL_SIZE
    x1 = x0 + CELL_SIZE - 1
    y1 = y0 + CELL_SIZE - 1
    draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255))

    return img

def move_snake(direction, snake):
    head_y, head_x = snake[0]
    if direction == "UP":
        head_y -= 1
    elif direction == "DOWN":
        head_y += 1
    elif direction == "LEFT":
        head_x -= 1
    elif direction == "RIGHT":
        head_x += 1
    return (head_y, head_x)

def place_food(snake):
    while True:
        pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if pos not in snake:
            return pos

# Initialize session state
if "snake" not in st.session_state:
    st.session_state.snake = [(10, 10), (10, 11), (10, 12)]
    st.session_state.food = place_food(st.session_state.snake)
    st.session_state.direction = "LEFT"
    st.session_state.score = 0
    st.session_state.running = False

st.title("🐍 Nokia-Style Snake Game")
difficulty = st.selectbox("Choose Difficulty", ["Easy", "Medium", "Hard"])

if st.button("Start Game"):
    st.session_state.running = True

# Arrow keys
col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.button("⬅️"):
        if st.session_state.direction != "RIGHT":
            st.session_state.direction = "LEFT"
with col2:
    if st.button("⬆️"):
        if st.session_state.direction != "DOWN":
            st.session_state.direction = "UP"
    if st.button("⬇️"):
        if st.session_state.direction != "UP":
            st.session_state.direction = "DOWN"
with col3:
    if st.button("➡️"):
        if st.session_state.direction != "LEFT":
            st.session_state.direction = "RIGHT"

if st.session_state.running:
    snake = st.session_state.snake
    new_head = move_snake(st.session_state.direction, snake)

    # Game over conditions
    if (new_head in snake or
        not (0 <= new_head[0] < GRID_SIZE and 0 <= new_head[1] < GRID_SIZE)):
        st.write(f"### Game Over! Your Score: {st.session_state.score}")
        st.session_state.running = False
    else:
        snake.insert(0, new_head)
        if new_head == st.session_state.food:
            st.session_state.food = place_food(snake)
            st.session_state.score += 1
        else:
            snake.pop()

    img = draw_board(snake, st.session_state.food)
    st.image(img)
    time.sleep(SPEED_MAP[difficulty])
    st.rerun()
