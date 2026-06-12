# ⚔ RPSLS Adversarial Search
**Rock · Paper · Scissors · Lizard · Spock — AI Game with Minimax & Alpha-Beta Pruning**

> Tugas Project Kecerdasan Buatan | S1 Teknik Informatika  
> Topik: Pencarian Adversarial (Game Playing)

---

## 🎮 Demo

🔗 **[Live Demo](https://namaanda.my.id)** *(ganti dengan URL deployment Anda)*

---

## ✨ Fitur

| # | Fitur | Status |
|---|-------|--------|
| 1 | Human vs AI (Minimax Algorithm) | ✅ |
| 2 | Alpha-Beta Pruning (optimasi Minimax) | ✅ |
| 3 | Visualisasi Game Tree (3 level) | ✅ |
| 4 | Counter node: Minimax vs Alpha-Beta | ✅ |
| 5 | Toggle Minimax murni vs Minimax+AB | ✅ |
| 6 | Pengaturan kedalaman pencarian (Depth 1–5) | ✅ |
| 7 | Indikator giliran & status permainan | ✅ |
| 8 | Tampilan responsif (desktop & mobile) | ✅ |
| 9 | **Bonus:** Mode Human vs Human | ✅ |

---

## 🧠 Tentang Algoritma

### Minimax
Minimax adalah algoritma pencarian adversarial yang bekerja pada **zero-sum game**.  
AI (MAX player) memilih langkah yang **memaksimalkan** skor, dengan asumsi lawan (MIN player) selalu memilih langkah yang **meminimalkan** skor AI.

```
minimax(node, depth, isMaximizing):
    if terminal(node): return evaluate(node)
    if isMaximizing:
        return max over children of minimax(child, depth-1, False)
    else:
        return min over children of minimax(child, depth-1, True)
```

### Alpha-Beta Pruning
Optimasi Minimax yang memangkas branch yang tidak mungkin memengaruhi keputusan akhir.  
- **α (alpha)**: nilai terbaik yang bisa dijamin MAX
- **β (beta)**: nilai terbaik yang bisa dijamin MIN
- Jika `β ≤ α` → branch dipangkas (tidak dievaluasi)

Efisiensi: memangkas **60–80%** node pada RPSLS di depth 3–5.

### RPSLS State Space
- 5 pilihan × 5 pilihan = **25 kombinasi outcome**
- Setiap ronde adalah game independen (single-shot game)
- Minimax optimal untuk menentukan probabilitas terbaik melawan lawan acak

---

## 🗂 Struktur Proyek

```
adversarial-search-[nim]/
├── app.py              ← Flask backend (Minimax, Alpha-Beta, REST API)
├── requirements.txt
├── README.md
└── templates/
    └── index.html      ← Frontend (HTML + CSS + JS)
```

---

## 🚀 Cara Menjalankan

### 1. Clone repository
```bash
git clone https://github.com/username/adversarial-search-reyna.git
cd adversarial-search-reyna
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Jalankan Flask
```bash
python app.py
```

### 4. Buka browser
```
http://localhost:5000
```

---

## 🌐 API Endpoints

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| `POST` | `/api/move` | Dapatkan langkah terbaik AI + node stats |
| `POST` | `/api/tree` | Dapatkan game tree JSON untuk visualisasi |
| `POST` | `/api/outcome` | Hitung hasil ronde (win/lose/draw) |
| `GET`  | `/api/rules` | Daftar aturan RPSLS |

### Contoh request `/api/move`:
```json
POST /api/move
{ "depth": 3, "use_ab": true }

Response:
{
  "best_move": "spock",
  "emoji": "🖖",
  "mm_nodes": 156,
  "ab_nodes": 62,
  "pruned": 94,
  "efficiency": 60.3,
  "elapsed_ms": 1.2
}
```

---

## 🔧 Stack Teknologi

- **Backend**: Python 3.10+ · Flask 3.x
- **Frontend**: HTML5 · CSS3 · Vanilla JavaScript
- **Algoritma**: Minimax · Alpha-Beta Pruning (diimplementasikan dari nol)
- **Hosting**: Domain `.my.id` (Niagahoster / IDCloudHost)
- **Version Control**: Git · GitHub

---

## 📚 Referensi

1. Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson. [Bab 5]
2. Silver, D., et al. (2016). Mastering the game of Go with deep neural networks. *Nature*, 529, 484–489.
3. Campbell, M., et al. (2002). Deep Blue. *Artificial Intelligence*, 134(1-2), 57–83.
4. Millington, I., & Funge, J. (2009). *AI for Games* (2nd ed.). Morgan Kaufmann.
5. MDN Web Docs. *JavaScript Reference*. https://developer.mozilla.org

---

## 👤 Author

**Reyna Noernaila** — 301240033 — 4A   
🔗 [LinkedIn](https://www.linkedin.com/in/reyna-noernaila-1b4827414/)
