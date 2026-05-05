import tkinter as tk
from tkinter import messagebox, simpledialog
import random

# ─────────────────────────────────────────────
#  COLORS & FONTS
# ─────────────────────────────────────────────
BG          = "#0f0f1a"
CELL_BG     = "#1a1a2e"
CELL_HOVER  = "#16213e"
X_COLOR     = "#e94560"
O_COLOR     = "#0f9b8e"
LINE_COLOR  = "#2a2a4a"
BTN_BG      = "#1a1a2e"
BTN_ACTIVE  = "#e94560"
TEXT_COLOR  = "#e0e0e0"
STATUS_COLOR= "#a0a0c0"
WIN_COLOR   = "#f5c518"

FONT_TITLE  = ("Courier New", 22, "bold")
FONT_CELL   = ("Courier New", 52, "bold")
FONT_STATUS = ("Courier New", 13)
FONT_BTN    = ("Courier New", 11, "bold")

# ─────────────────────────────────────────────
#  AI — Minimax with alpha-beta
# ─────────────────────────────────────────────
WINNING_LINES = [
    (0,1,2),(3,4,5),(6,7,8),
    (0,3,6),(1,4,7),(2,5,8),
    (0,4,8),(2,4,6),
]

def check_winner(board):
    for a,b,c in WINNING_LINES:
        if board[a] == board[b] == board[c] != "":
            return board[a], (a,b,c)
    if "" not in board:
        return "draw", None
    return None, None

def minimax(board, is_max, alpha, beta, depth):
    winner, _ = check_winner(board)
    if winner == "O": return 10 - depth
    if winner == "X": return depth - 10
    if winner == "draw": return 0

    if is_max:
        best = -100
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                best = max(best, minimax(board, False, alpha, beta, depth+1))
                board[i] = ""
                alpha = max(alpha, best)
                if beta <= alpha: break
        return best
    else:
        best = 100
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                best = min(best, minimax(board, True, alpha, beta, depth+1))
                board[i] = ""
                beta = min(beta, best)
                if beta <= alpha: break
        return best

def ai_move(board, difficulty):
    free = [i for i,v in enumerate(board) if v == ""]
    if difficulty == "Easy":
        return random.choice(free)
    if difficulty == "Medium" and random.random() < 0.4:
        return random.choice(free)
    best_score, best_idx = -100, random.choice(free)
    for i in free:
        board[i] = "O"
        s = minimax(board, False, -100, 100, 0)
        board[i] = ""
        if s > best_score:
            best_score, best_idx = s, i
    return best_idx

# ─────────────────────────────────────────────
#  MAIN APPLICATION
# ─────────────────────────────────────────────
class TicTacToe(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic Tac Toe")
        self.resizable(False, False)
        self.configure(bg=BG)
        self._show_menu()

    # ── MENU SCREEN ──────────────────────────
    def _show_menu(self):
        self._clear_window()
        self.geometry("380x480")

        tk.Label(self, text="TIC TAC TOE", font=FONT_TITLE,
                 bg=BG, fg=X_COLOR).pack(pady=(40,4))
        tk.Label(self, text="─" * 28, font=("Courier New",10),
                 bg=BG, fg=LINE_COLOR).pack()

        tk.Label(self, text="Choose Mode", font=FONT_STATUS,
                 bg=BG, fg=STATUS_COLOR).pack(pady=(30,16))

        self._menu_btn("👥  Two Players",  self._setup_two_player)
        tk.Label(self, text="", bg=BG).pack(pady=4)
        self._menu_btn("🤖  vs AI",        self._setup_vs_ai)

        tk.Label(self, text="", bg=BG).pack(expand=True)
        tk.Label(self, text="built with tkinter  •  python",
                 font=("Courier New",9), bg=BG, fg="#444466").pack(pady=12)

    def _menu_btn(self, text, cmd):
        b = tk.Button(self, text=text, font=FONT_BTN,
                      bg=BTN_BG, fg=TEXT_COLOR,
                      activebackground=BTN_ACTIVE, activeforeground="white",
                      relief="flat", bd=0, padx=28, pady=14,
                      cursor="hand2", command=cmd)
        b.pack(ipadx=20)
        b.bind("<Enter>", lambda e: b.config(bg=BTN_ACTIVE, fg="white"))
        b.bind("<Leave>", lambda e: b.config(bg=BTN_BG,     fg=TEXT_COLOR))

    # ── SETUP SCREENS ────────────────────────
    def _setup_two_player(self):
        self._clear_window()
        self.geometry("380x400")

        tk.Label(self, text="Two Players", font=FONT_TITLE,
                 bg=BG, fg=X_COLOR).pack(pady=(36,20))

        self.p1_var = tk.StringVar(value="Player 1")
        self.p2_var = tk.StringVar(value="Player 2")

        for label, var, color in [
            ("Player 1  (X)", self.p1_var, X_COLOR),
            ("Player 2  (O)", self.p2_var, O_COLOR),
        ]:
            tk.Label(self, text=label, font=FONT_STATUS, bg=BG, fg=color).pack(pady=(12,2))
            e = tk.Entry(self, textvariable=var, font=FONT_STATUS,
                         bg=CELL_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR,
                         relief="flat", bd=0, width=22, justify="center")
            e.pack(ipady=6)

        tk.Label(self, text="", bg=BG).pack(pady=8)
        self._menu_btn("▶  Start Game",
                       lambda: self._start_game("2p", None,
                                                self.p1_var.get() or "Player 1",
                                                self.p2_var.get() or "Player 2"))
        tk.Label(self, text="", bg=BG).pack(pady=4)
        self._menu_btn("← Back", self._show_menu)

    def _setup_vs_ai(self):
        self._clear_window()
        self.geometry("380x420")

        tk.Label(self, text="vs AI", font=FONT_TITLE,
                 bg=BG, fg=O_COLOR).pack(pady=(36,20))

        self.p1_var = tk.StringVar(value="Player")
        tk.Label(self, text="Your Name  (X)", font=FONT_STATUS, bg=BG, fg=X_COLOR).pack(pady=(8,2))
        e = tk.Entry(self, textvariable=self.p1_var, font=FONT_STATUS,
                     bg=CELL_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR,
                     relief="flat", bd=0, width=22, justify="center")
        e.pack(ipady=6)

        tk.Label(self, text="Difficulty", font=FONT_STATUS, bg=BG, fg=STATUS_COLOR).pack(pady=(20,6))
        self.diff_var = tk.StringVar(value="Hard")
        frm = tk.Frame(self, bg=BG)
        frm.pack()
        for lvl, col in [("Easy", O_COLOR), ("Medium", WIN_COLOR), ("Hard", X_COLOR)]:
            rb = tk.Radiobutton(frm, text=lvl, variable=self.diff_var, value=lvl,
                                font=FONT_BTN, bg=BG, fg=col,
                                activebackground=BG, selectcolor=BG,
                                indicatoron=0, relief="flat", padx=14, pady=6,
                                cursor="hand2")
            rb.pack(side="left", padx=6)

        tk.Label(self, text="", bg=BG).pack(pady=8)
        self._menu_btn("▶  Start Game",
                       lambda: self._start_game("ai", self.diff_var.get(),
                                                self.p1_var.get() or "Player", "AI"))
        tk.Label(self, text="", bg=BG).pack(pady=4)
        self._menu_btn("← Back", self._show_menu)

    # ── GAME SCREEN ──────────────────────────
    def _start_game(self, mode, difficulty, p1_name, p2_name):
        self._clear_window()
        self.geometry("420x560")

        self.mode       = mode
        self.difficulty = difficulty
        self.p_names    = [p1_name, p2_name]
        self.board      = [""] * 9
        self.current    = 0     # 0 = X, 1 = O
        self.game_over  = False
        self.buttons    = []

        # ── header ──
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", padx=24, pady=(20,0))
        self.lbl_x = tk.Label(hdr, text=f"✕  {p1_name}",
                              font=FONT_STATUS, bg=BG, fg=X_COLOR)
        self.lbl_x.pack(side="left")
        self.lbl_o = tk.Label(hdr, text=f"{p2_name}  ○",
                              font=FONT_STATUS, bg=BG, fg=STATUS_COLOR)
        self.lbl_o.pack(side="right")

        # ── status ──
        self.status_var = tk.StringVar()
        tk.Label(self, textvariable=self.status_var, font=FONT_STATUS,
                 bg=BG, fg=STATUS_COLOR).pack(pady=(8,0))

        # ── grid ──
        grid_frame = tk.Frame(self, bg=LINE_COLOR, padx=3, pady=3)
        grid_frame.pack(padx=24, pady=12)

        for i in range(9):
            r, c = divmod(i, 3)
            btn = tk.Button(grid_frame, text="", font=FONT_CELL,
                            width=3, height=1,
                            bg=CELL_BG, fg=TEXT_COLOR,
                            activebackground=CELL_HOVER,
                            relief="flat", bd=0, cursor="hand2",
                            command=lambda idx=i: self._on_click(idx))
            btn.grid(row=r, column=c, padx=2, pady=2, ipadx=6, ipady=6)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=CELL_HOVER) if b["text"]=="" else None)
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=CELL_BG))
            self.buttons.append(btn)

        # ── bottom buttons ──
        bot = tk.Frame(self, bg=BG)
        bot.pack(pady=4)
        for txt, cmd in [("🔄  Restart", self._restart),
                         ("🏠  Menu",    self._show_menu)]:
            b = tk.Button(bot, text=txt, font=FONT_BTN,
                          bg=BTN_BG, fg=TEXT_COLOR,
                          activebackground=BTN_ACTIVE, activeforeground="white",
                          relief="flat", bd=0, padx=16, pady=8,
                          cursor="hand2", command=cmd)
            b.pack(side="left", padx=8)
            b.bind("<Enter>", lambda e, b=b: b.config(bg=BTN_ACTIVE, fg="white"))
            b.bind("<Leave>", lambda e, b=b: b.config(bg=BTN_BG,     fg=TEXT_COLOR))

        self._update_status()

    def _update_status(self):
        symbol = ["X", "O"][self.current]
        name   = self.p_names[self.current]
        color  = [X_COLOR, O_COLOR][self.current]
        self.status_var.set(f"{name}'s turn  ({symbol})")
        self.lbl_x.config(fg=X_COLOR if self.current==0 else STATUS_COLOR)
        self.lbl_o.config(fg=O_COLOR  if self.current==1 else STATUS_COLOR)

    def _on_click(self, idx):
        if self.game_over or self.board[idx] != "":
            return
        self._make_move(idx)
        if not self.game_over and self.mode == "ai" and self.current == 1:
            self.after(300, self._ai_turn)

    def _make_move(self, idx):
        symbol = ["X", "O"][self.current]
        color  = [X_COLOR, O_COLOR][self.current]
        self.board[idx] = symbol
        self.buttons[idx].config(text=symbol, fg=color,
                                 disabledforeground=color, state="disabled")

        winner, line = check_winner(self.board)
        if winner:
            self._end_game(winner, line)
        else:
            self.current = 1 - self.current
            self._update_status()

    def _ai_turn(self):
        if self.game_over:
            return
        idx = ai_move(self.board, self.difficulty)
        self._make_move(idx)

    def _end_game(self, winner, line):
        self.game_over = True
        if winner == "draw":
            self.status_var.set("It's a Draw! 🤝")
            for b in self.buttons:
                b.config(cursor="arrow")
        else:
            name = self.p_names[0 if winner=="X" else 1]
            self.status_var.set(f"{name} Wins! 🎉")
            if line:
                for i in line:
                    self.buttons[i].config(bg=WIN_COLOR, fg="#0f0f1a",
                                           disabledforeground="#0f0f1a")
        # disable all remaining cells
        for b in self.buttons:
            b.config(state="disabled", cursor="arrow")

    def _restart(self):
        self._start_game(self.mode, self.difficulty,
                         self.p_names[0], self.p_names[1])

    def _clear_window(self):
        for w in self.winfo_children():
            w.destroy()


# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = TicTacToe()
    app.mainloop()
