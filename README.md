🌟 Genshin Impact Team Optimizer — Luna IV
Version 0.2 Beta

A Python-based team rotation optimizer for Genshin Impact that helps players build the best 4-character team based on elements, roles, weapons, and elemental reactions — all powered by a structured Excel database.
Built for players who want logic-backed team building, not just vibes.

🎮 What Is This?
This tool analyzes your available characters and finds the optimal team rotation by maximizing elemental reaction multipliers, while respecting team composition rules such as:
- Main DPS
- Sub DPS
- Healer / Shield
- Weapon & Element constraints
It is designed to be:
- Beginner-friendly 👶
- Flexible for late-game players ⚔️
- Understandable for developers 👨‍💻👩‍💻

✨ Features (v0.2 Beta)
✅ Inventory input using nicknames
✅ Weapon filtering (Sword, Claymore, Bow, Catalyst, Polearm)
✅ Element exclusion filter
✅ Role-based team validation
✅ Build choice selection
✅ Best team rotation order (1 → 4)

🧠 How the Optimizer Thinks
1. Load & clean database
2. Ask user for owned characters
3. Apply weapon filters
4. Apply element exclusion
5. (Optional) Enforce role rules
6. Resolve dual-role characters (build choice)
7. Generate all valid 4-character teams
8. Test all possible rotations
9. Pick the team with the highest reaction multiplier score
📌 A detailed flowchart is included in this repository for reference.

📁 genshin-team-optimizer/
│
├── calc.py                        # Main optimizer script
├── Genshin_DB-ver_Luna_IV         # Database (latest game version)
├── Inventory_Optimizer-v0.2-beta  # Logic flowchart
├── README.md                      # This file

▶️ How to Run
Requirements:
1. Python 3.10+ 
2. pandas

Steps:
1. Download the files and put it on 1 folder
2. Open the calc.py file
3. On the terminal, type "pip install pandas"
4. On the terminal, type "python calc.py"
5. Follow the prompts on the terminal

🌐 Future Plan: Streamlit Web App
This optimizer is planned to be deployed as a Streamlit web app.
Stay tuned 👀

🤝 Contribution & Feedback
Feedback is very welcome! If you’re a programmer or theorycrafter and see something off — please open an issue or PR 🙏

⚠️ DISCLAIMER
This project is:
- Fan-made
- Non-commercial
- Not affiliated with HoYoverse
- All character data belongs to Genshin Impact.


And good luck on your Genshin journey, Traveler!
