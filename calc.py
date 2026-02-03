import pandas as pd
import itertools

#LOAD DB
file_path = "Genshin_DB-ver_Luna_IV.xlsx"

df_role = pd.read_excel(file_path, sheet_name="DB_ROLE")
df_char = pd.read_excel(file_path, sheet_name="DB_CHARACTER")
df_react = pd.read_excel(file_path, sheet_name="DB_EReac")

role_columns = [
    "DPS",
    "On-field",
    "Off-field",
    "Support",
    "Survivability"
]

has_role=df_role[role_columns].eq("Yes").any(axis=1)

df_role_ref = df_role[has_role].copy()

valid_names = set(df_role_ref["Name"])
df_char_clean = df_char[df_char["Name"].isin(valid_names)].copy()
df_char_ref = df_char_clean.loc[:, ~df_char_clean.columns.str.contains('^Unnamed')]

with pd.ExcelWriter("Filtered_Genshin_DB.xlsx") as writer:
    df_role_ref.to_excel(writer, sheet_name="DB_ROLE_REF", index=False)
    df_char_ref.to_excel(writer, sheet_name="DB_CHAR_REF", index=False)

#INPUT INVENTORY
def resolve_character_name(user_input, df):
    matches = df[df["Name"].str.contains(user_input, case=False, na=False)]["Name"].unique()
    if len(matches) == 0:
        print(f"❌ No matches found for '{user_input}'. Please try again.")
        return None
    elif len(matches) > 1:
        print(f"⚠️ Multiple matches found for '{user_input}'. Matches found:")
        for name in matches:
            print(f"- {name}")
        print("Please enter a more specific name.")
        return None
    else:
        return matches[0]

print("WELCOME TO THE GENSHIN IMPACT VERSION LUNA IV TEAM OPTIMIZER 0.2 BETA!")

def ask_character(df):
    while True:
        user_input = input("Enter character name (nickname allowed): ").strip()
        result = resolve_character_name(user_input, df)
        if result is not None:
            print(f"✅ Thank you! You have selected: {result}")
            return result
        
def ask_inventory(df, max_chars=20):
    inventory = []
    print(f"\nPlease enter up to {max_chars} character names for your inventory.") 
    print("Type 'done' when you are finished.\n")

    while len(inventory) < max_chars:
        user_input = input(f"Enter character name (or 'done' to finish): ").strip()
        if user_input.lower() == 'done':
            break
        resolved = resolve_character_name(user_input, df)
        if resolved:
            if resolved in inventory:
                print(f"⚠️ '{resolved}' is already in your inventory. Please enter a different character.")
            else:
                inventory.append(resolved)
                print(f"✅ '{resolved}' added to your inventory.")
    return inventory

inventory = ask_inventory(df_char_ref)
print("\nYour final inventory: ")
for i, name in enumerate(inventory, start=1):
    print(f"{i}. {name}")
print("\n")

char_to_element = dict(zip(df_char_ref["Name"], df_char_ref["Element"]))
reaction_multiplier = {
    (row["First Element"], row["Second Element"]): row["Multiplier"]
    for _, row in df_react.iterrows()
}

#FILTER WEAPON
weapon_options = ["Sword", "Claymore", "Polearm", "Bow", "Catalyst"]
print("\nChoose weapons to INCLUDE (use commas)")
for i, w in enumerate(weapon_options, 1):
    print(f"{i}. {w}")

weapon_input = input("Enter numbers (e.g., 1,3 for Sword and Polearm): ")

selected_weapon_indices = [
    int(x.strip()) - 1 for x in weapon_input.split(",") if x.strip().isdigit() and 1 <= int(x.strip()) <= len(weapon_options)
]
selected_weapons = [weapon_options[i] for i in selected_weapon_indices
                    if 0 <= i < len(weapon_options)]
if not selected_weapons:
    print("No valid weapons selected. Exiting.")
    exit()

char_to_weapon = dict(zip(df_char_ref["Name"], df_char_ref["Weapon"]))
filtered_inventory = [
    c for c in inventory if char_to_weapon[c] in selected_weapons
]

if len(filtered_inventory) < 4:
    print("Not enough characters with the selected weapons. Exiting.")
    exit()

#FILTER ROLE
role_lookup = df_role.set_index("Name")[[
    "DPS",
    "On-field",
    "Off-field",
    "Support",
    "Survivability"
]].to_dict(orient="index")

def can_be_main_dps(char):
    r = role_lookup[char]
    return r["DPS"] == "Yes" and r["On-field"] == "Yes"

def can_be_sub_dps(char):
    r = role_lookup[char]
    return r["DPS"] == "Yes" and r["Off-field"] == "Yes"

def can_be_healer(char):
    return role_lookup[char]["Survivability"] == "Yes"

def can_be_shield(char):
    r = role_lookup[char]
    return r["Survivability"] == "Yes" or r["Support"] == "Yes"

def possible_roles(char):
    roles = []
    if can_be_main_dps(char):
        roles.append("Main DPS")
    if can_be_sub_dps(char):
        roles.append("Sub DPS")
    if can_be_healer(char):
        roles.append("Healer")
    if can_be_shield(char):
        roles.append("Shield")
    return roles


#FILTER ELEMENT
element_filter = ["PYRO", "HYDRO", "ELECTRO", "CRYO", "ANEMO", "GEO", "DENDRO"]
characters = filtered_inventory

print("\nChoose elements to EXCLUDE (use commas)")
print("Press ENTER to include ALL elements")

for i, e in enumerate(element_filter, 1):
    print(f"{i}. {e}")
user_input = input("Enter numbers: ")

if user_input.strip() == "":
    excluded_elements = []
else:
    excluded_indices = [
        int(x.strip()) - 1 for x in user_input.split(",") 
        if x.strip().isdigit() and 1 <= int(x.strip()) <= len(element_filter)
    ]
    excluded_elements = [element_filter[i] for i in excluded_indices]


filtered_characters = [
    c for c in characters
    if char_to_element[c].upper() not in excluded_elements
]
if len(filtered_characters) < 4:
    print("Not enough characters with the selected elements. Exiting.")
    exit()


while True:
    role_choice = input("\nDo you want to optimize character roles [NOT RECOMMENDED FOR BEGINNER]? (yes/no): ").strip().lower()
    if role_choice in ["y", "yes"]:
        use_role_optimization = True
        break
    elif role_choice in ["n", "no"]:
        use_role_optimization = False
        break
    else:
        print("Invalid input. Please enter 'yes' or 'no'.")

#ROLE CONDITIONER
def valid_team(team):
    if not use_role_optimization:
        return True
    has_main = any(choosen_role[c] == "Main DPS" for c in team)
    has_sub = any(choosen_role[c] == "Sub DPS" for c in team)
    has_survive = any(choosen_role[c] in ["Healer", "Shield"] for c in team)
    return has_main and has_sub and has_survive

choosen_role = {}
if not use_role_optimization:
    print("\nCharacter Build Configuration")
    for char in filtered_characters:
        roles = possible_roles(char)

        has_dps = any(r in ["Main DPS", "Sub DPS"] for r in roles)
        has_survivability = any(r in ["Healer", "Shield"] for r in roles)

        if has_dps and has_survivability:
            print(f"\n{char} can be build in multiple ways.")
            for i, r in enumerate(roles, 1):
                print(f"{i}. {r}")
            while True:
                choice = input(f"Choose role for {char} (1-{len(roles)}): ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(roles):
                    choosen_role[char] = roles[int(choice) - 1]
                    break
                else:
                    print("Invalid choice. Please try again.")
        else:
            choosen_role[char] = roles[0] if roles else "None"
else:
    for char in filtered_characters:
        choosen_role[char] = "Any"

#OPTIMIZER ENGINE
def rotation_score(rotation):
    score=0
    for i in range(len(rotation) - 1):
        elem1 = char_to_element[rotation[i]]
        elem2 = char_to_element[rotation[i + 1]]
        score += reaction_multiplier.get((elem1, elem2), 0)
    return score    
best_team = None
best_score = -1
    
for team in itertools.combinations(filtered_characters, 4):

    if not valid_team(team):
        continue
    
    for rotation in itertools.permutations(team):
        score = rotation_score(rotation)
        if score > best_score:
            best_score = score
            best_team = rotation

def is_main_dps(char):
    return choosen_role.get(char) == "Main DPS"

def is_sub_dps(char):
    return choosen_role.get(char) == "Sub DPS"

def is_healer(char):
    return choosen_role.get(char) == "Healer"

def is_shield(char):
    return choosen_role.get(char) == "Shield"

print("\n 🔥Optimal Team Composition:🔥")
if best_team is None:
    print("No valid team could be formed with the given constraints.")
    print("Try include more weapon or enter different characters.")
    exit()
for i, char in enumerate(best_team, 1):
    print(f"{i}. {char} ({char_to_element[char]}) → {choosen_role[char]}")
print(f"Total Elemental Multiplier Score: {best_score}")
print("\n GOOD LUCK ON YOUR GENSHTIN JOURNEY! 🌟")
print()


