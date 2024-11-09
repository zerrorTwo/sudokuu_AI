import tkinter as tk
from tkinter import messagebox
import time

# bảng sudoku đầu vào 
sudoku_board = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 0],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]

# Hàm thuaatj toán 
def backtracking_sudoku(sudoku_board):
    # đi tìm các ô trống còn thiếu
    empty = find_space(sudoku_board)
    # Nếu đã tìm được tất cả các ô phù hợp thì dừng thuật toán
    if not empty:
        return True
    row, col = empty

    # Tìm số phù hợp để điền
    for num in range(1, 10):
        # kiểm tra tính hợp lệ của số đó theo điều kiện
        if valid_number(sudoku_board, num, (row, col)):
            sudoku_board[row][col] = num
            update_sudoku_board(sudoku_board)  # update giao diện 
            time.sleep(0.1)  

        # đệ quy tìm số để điền tiếp theo, nếu không phù hợp gán số cha bằng 0 và tiếp tục tìm số phù hợp cho ô đó
            if backtracking_sudoku(sudoku_board):
                return True

            sudoku_board[row][col] = 0
            update_sudoku_board(sudoku_board)  # Xóa số không hợp lệ và cập nhật GUI
            time.sleep(0.1)  # Tạm dừng để hiển thị từng bước
    # Nếu 1 ô không thể điền bất kỳ số nào thì không thể giải
    return False

# Đi tìm tính hợp lệ của số cần điền
def valid_number(sudoku_board, num, pos):
    row, col = pos

    # check trên hàng 
    if any(sudoku_board[row][i] == num for i in range(9)):
        return False

    # check trên cột
    if any(sudoku_board[i][col] == num for i in range(9)):
        return False

    # check trên phạm vi 3x3 của ô đó
    _x, _y = col // 3, row // 3 
    for i in range(_y * 3, _y * 3 + 3):
        for j in range(_x * 3, _x * 3 + 3):
            if sudoku_board[i][j] == num:
                return False

    return True

# Tìm ô trống để điền
def find_space(sudoku_board):
    for i in range(9):
        for j in range(9):
            if sudoku_board[i][j] == 0:
                return (i, j)
    return None

# hàm UI để hiển thị bảng 
def get_sudoku_board():
    sudoku_board = []
    for i in range(9):
        row = []
        for j in range(9):
            entry_val = entries[i][j].get()
            row.append(int(entry_val) if entry_val.isdigit() else 0)
        sudoku_board.append(row)
    return sudoku_board

# update GUI 
def update_sudoku_board(sudoku_board):
    for i in range(9):
        for j in range(9):
            entries[i][j].delete(0, tk.END)
            if sudoku_board[i][j] != 0:
                entries[i][j].insert(0, str(sudoku_board[i][j]))
    root.update()  # Cập nhật giao diện ngay lập tức

# Hàm triển khai thuật toán
def solve():
    sudoku_board = get_sudoku_board()
    if backtracking_sudoku(sudoku_board):
        messagebox.showinfo("Thành công", "Sudoku đã được giải!")
    else:
        messagebox.showerror("Lỗi", "Không thể giải Sudoku.")

# ------------------------------ GUI --------------------------------------
def display_initial_sudoku_board(sudoku_board):
    for i in range(9):
        for j in range(9):
            if sudoku_board[i][j] != 0:
                entries[i][j].insert(0, str(sudoku_board[i][j]))


root = tk.Tk()
root.title("Sudoku Solver")
entries = [[None for _ in range(9)] for _ in range(9)]

# Tạo giao diện cho bảng 9x9
for i in range(9):
    for j in range(9):
        entry = tk.Entry(root, width=2, font=("Arial", 18), justify="center")
        entry.grid(row=i, column=j, padx=5, pady=5)
        entries[i][j] = entry

# Hiển thị sudoku đầu vào
display_initial_sudoku_board(sudoku_board)

# nút để giải
solve_button = tk.Button(root, text="Backtracking", command=solve)
solve_button.grid(row=10, column=3, columnspan=3)

root.mainloop()

# -------------------------- END GUI --------------------------------------
