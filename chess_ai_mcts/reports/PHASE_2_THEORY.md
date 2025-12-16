## GIAI ĐOẠN 2: CƠ SỞ LÝ THUYẾT

### I. Giới thiệu về MCTS (Monte Carlo Tree Search)

#### 1. Khái niệm cơ bản
MCTS là một thuật toán tìm kiếm dựa trên các phương pháp Monte Carlo, được sử dụng để tìm kiếm cây quyết định trong các trò chơi.

**Ưu điểm chính:**
- Không cần heuristic phức tạp (có thể chơi mù)
- Hiệu quả với không gian tìm kiếm lớn
- Dễ song song hóa
- Ngoại suy tự động từ lịch sử

**Nhược điểm:**
- Cần nhiều thời gian / lần lặp
- Có thể chậm trong các giai đoạn cuối ván

#### 2. Bốn bước chính của MCTS

```
        ROOT (starting position)
         /    |    \
     Move1  Move2  Move3  ... [UCT Selection]
      /        |       \
   Node1    Node2    Node3    [Expansion: add children]
    
    Simulate random game from selected node
    
    Backpropagate result up the tree
```

**Bước 1: Selection (Lựa chọn)**
- Bắt đầu từ root
- Dùng công thức UCT (Upper Confidence bounds applied to Trees) để chọn nút con
- UCT = (Q/N) + C * sqrt(ln(P) / N)
  - Q: tổng reward
  - N: số lần visited
  - P: parent visits
  - C: exploration constant (thường sqrt(2) ≈ 1.41)

**Bước 2: Expansion (Mở rộng)**
- Nếu nút hiện tại chưa được phát triển hết
- Chọn 1 nước chưa thử từ danh sách nước hợp lệ
- Thêm nút con mới vào cây

**Bước 3: Simulation (Mô phỏng)**
- Từ nút mới, chơi random đến hết ván
- Mỗi nước được chọn ngẫu nhiên từ nước hợp lệ

**Bước 4: Backpropagation (Lan truyền)**
- Cập nhật kết quả từ dưới lên tất cả tổ tiên
- N += 1 (increment visit count)
- Q += reward (accumulate reward)

#### 3. Công thức UCT Chi tiết

```
UCT(node) = Average_Value(node) + C * sqrt(ln(parent.visits) / node.visits)
          = W/N + C * sqrt(ln(N_parent) / N)
```

**Phân tích:**
- **W/N (Exploitation)**: tỷ lệ thắng của nút → ưu tiên nút tốt
- **C * sqrt(ln(P)/N) (Exploration)**: khám phá nút ít được thăm
- **C = sqrt(2)**: cân bằng giữa khai thác và khám phá

### II. So sánh MCTS vs Minimax

| Tiêu chí | MCTS | Minimax |
|---------|------|---------|
| **Heuristic** | Không cần (random simulation) | Cần evaluation function phức tạp |
| **Không gian tìm kiếm** | Hiệu quả với không gian lớn | Phụ thuộc độ sâu |
| **Tính toán** | Xác suất (Monte Carlo) | Deterministic |
| **Tốc độ** | Chậm ban đầu, nhanh với thời gian | Nhanh ban đầu, chậm với không gian lớn |
| **Tiện nghi** | Dễ song song | Khó song song (alpha-beta) |
| **Ứng dụng** | Go, Cờ vua (AlphaGo) | Cờ vua cổ điển |
| **Độ sâu** | Có thể vô hạn | Giới hạn bởi thời gian/độ sâu |

### III. AlphaBeta Pruning (Cải tiến Minimax)

AlphaBeta cắt bớt các nhánh không cần thiết:

```
alpha = best score for maximizer so far
beta = best score for minimizer so far

If alpha >= beta: cut off remaining branches
```

**Hiệu suất:**
- Tốt nhất: O(b^(d/2)) thay vì O(b^d)
- Trung bình: O(b^(3d/4))
- Tồi nhất: O(b^d)

### IV. Các biến thể MCTS

1. **Pure MCTS**: Chỉ dùng simulation random
2. **MCTS + Heuristic**: Dùng evaluation function tốt hơn
3. **AlphaZero-lite**: MCTS + Neural Network
4. **Rapid Action Value Estimation (RAVE)**: Dùng all-moves-as-first (AMAF)

### V. Các tham số quan trọng

```python
# Exploration constant
C = sqrt(2)  # ≈ 1.41 (balance exploration/exploitation)

# Time/Iteration budget
- time_limit: 1-10 giây per move
- iterations: 100-10000 iterations

# Simulation depth
- random playout: play to terminal state
- limited depth: play K moves then evaluate
```

### VI. Tại sao MCTS hiệu quả trong cờ vua?

1. **Không cần evaluation function**: random simulation cho kết quả khá
2. **Tự thích nghi**: học cấu trúc ván từ data
3. **Có thể mở rộng**: càng nhiều thời gian càng tốt
4. **Balanced**: không rơi vào trap cục bộ như greedy

### VII. Kết luận

**MCTS là tốt cho:**
- Trò chơi với không gian tìm kiếm lớn (Go, cờ vua)
- Khi không có evaluation function tốt
- Khi muốn hiệu quả thời gian cao

**Minimax tốt cho:**
- Không gian tìm kiếm nhỏ đến trung bình
- Khi có evaluation function tốt
- Khi độ sâu yêu cầu là hạn chế

---

**Tham khảo:**
- Browne et al. (2012) - A Survey of Monte Carlo Tree Search Methods
- AlphaGo Paper - Mastering the game of Go
- Russell & Norvig - AI: A Modern Approach
