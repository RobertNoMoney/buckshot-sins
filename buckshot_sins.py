import streamlit as st
import random, time

st.set_page_config(page_title="Buckshot Roulette: Seven Sins", page_icon="💀", layout="centered")

# 🎲 Data dasar
sins = ["Pride", "Gluttony", "Envy", "Lust", "Wrath", "Sloth", "Greed"]
sin_heart = {
    "Pride": "🧡", "Gluttony": "💜", "Envy": "💚",
    "Lust": "💗", "Wrath": "❤️", "Sloth": "💙", "Greed": "💛"
}
tools_list = ["🔍 Kaca Pembesar", "🧃 Cola", "🩹 Perban", "🔗 Borgol"]

# ================= GACHA DOSA ==================
def gacha_sin_ui(player_name):
    st.subheader(f"{player_name}, giliran gacha dosa!")
    if st.button(f"🎰 Mulai Gacha ({player_name})"):
        placeholder = st.empty()
        for _ in range(20):
            spin = random.choice(sins)
            placeholder.markdown(f"### {sin_heart[spin]} {spin}")
            time.sleep(0.08)
        result = random.choice(sins)
        placeholder.markdown(f"## ✨ {player_name} mendapatkan {sin_heart[result]} **{result}!** ✨")
        return result
    return None

# ================= GAME LOGIC ==================
def random_tools():
    return random.sample(tools_list, 4)

def shoot(attacker, defender):
    st.write(f"🔫 {attacker['name']} menembak...")
    time.sleep(1)
    if random.randint(1, 100) <= 50:
        dmg = 1
        if attacker["sin"] == "Pride" and attacker.get("buff"):
            dmg *= 2
            attacker["buff"] = False
            attacker["hp"] += 0.5
            st.write("🧡 Pride memulihkan 0.5 HP karena tembakan 2x damage berhasil!")
        if attacker["sin"] == "Wrath" and attacker.get("marah"):
            dmg *= 2
            attacker["marah"] = False
        defender["hp"] -= dmg
        st.write(f"💥 Tembakan kena! {defender['name']} kehilangan {dmg} HP!")
        if defender["sin"] == "Envy" and random.randint(1, 100) <= 70:
            st.write("💚 Envy iri! Membalas serangan dengan 1.5 damage!")
            attacker["hp"] -= 1.5
    else:
        st.write("💨 Peluru meleset!")
        if attacker["sin"] == "Pride":
            attacker["buff"] = True
            st.write("🧡 Pride buff aktif! 2x damage untuk tembakan berikutnya!")
        if defender["sin"] == "Gluttony":
            st.write("💜 Gluttony menyedot 0.5 HP dari penyerang!")
            attacker["hp"] -= 0.5
            defender["hp"] += 0.5

def use_tool(player, opponent):
    tool_choice = st.radio("Pilih tools:", player["tools"], index=None)
    if st.button(f"Gunakan tools ({player['name']})"):
        if tool_choice:
            player["tools"].remove(tool_choice)
            st.write(f"🧰 {player['name']} menggunakan {tool_choice}!")

            if "Perban" in tool_choice:
                player["hp"] += 1
                st.write("🩹 HP bertambah 1!")
            elif "Borgol" in tool_choice:
                opponent["skip"] = True
                st.write("🔗 Lawan kehilangan 1 giliran!")
            elif "Kaca" in tool_choice:
                st.write("🔍 Kamu mengintip peluru... (efek imajiner)")
            elif "Cola" in tool_choice:
                st.write("🧃 Cola membuang satu peluru... (efek imajiner)")

            if opponent["sin"] == "Envy" and random.randint(1, 100) <= 70:
                st.write("💚 Envy ikut menggunakan efek item yang sama!")
        else:
            st.warning("Pilih tools terlebih dahulu!")

# ================= MAIN STREAMLIT ==================
st.title("💀 Buckshot Roulette: Seven Sins Edition 💀")

if "phase" not in st.session_state:
    st.session_state.phase = "gacha1"
    st.session_state.player1 = {"name": "Player 1", "hp": 5, "sin": None, "tools": random_tools(), "buff": False, "marah": False, "skip": False}
    st.session_state.player2 = {"name": "Player 2", "hp": 5, "sin": None, "tools": random_tools(), "buff": False, "marah": False, "skip": False}
    st.session_state.turn = 1

# === PHASE GACHA ===
if st.session_state.phase == "gacha1":
    sin = gacha_sin_ui("Player 1")
    if sin:
        st.session_state.player1["sin"] = sin
        st.session_state.phase = "gacha2"

elif st.session_state.phase == "gacha2":
    sin = gacha_sin_ui("Player 2")
    if sin:
        st.session_state.player2["sin"] = sin
        st.session_state.phase = "battle"

# === PHASE BATTLE ===
elif st.session_state.phase == "battle":
    p1 = st.session_state.player1
    p2 = st.session_state.player2

    st.markdown("---")
    st.subheader("📊 Status Pemain")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**{p1['name']}** {sin_heart[p1['sin']]} {p1['sin']}")
        st.progress(p1["hp"] / 5)
        st.write("Tools:", ", ".join(p1["tools"]))
    with col2:
        st.write(f"**{p2['name']}** {sin_heart[p2['sin']]} {p2['sin']}")
        st.progress(p2["hp"] / 5)
        st.write("Tools:", ", ".join(p2["tools"]))

    st.markdown("---")
    current = p1 if st.session_state.turn % 2 == 1 else p2
    opponent = p2 if current == p1 else p1

    st.subheader(f"🎯 Giliran: {current['name']} ({sin_heart[current['sin']]} {current['sin']})")

    act = st.radio("Pilih aksi:", ["Tembak", "Pakai Tools"], index=None)

    if st.button("Lanjut!"):
        if act == "Tembak":
            shoot(current, opponent)
        elif act == "Pakai Tools":
            use_tool(current, opponent)
        else:
            st.warning("Pilih aksi dulu!")

        if opponent["hp"] <= 0:
            st.session_state.phase = "end"
        else:
            st.session_state.turn += 1

# === PHASE END ===
elif st.session_state.phase == "end":
    p1 = st.session_state.player1
    p2 = st.session_state.player2
    st.subheader("🏁 Pertarungan Selesai!")

    if p1["hp"] <= 0 and p2["hp"] <= 0:
        st.write("🤝 Seri!")
    elif p1["hp"] <= 0:
        st.success("🏆 Player 2 menang!")
    else:
        st.success("🏆 Player 1 menang!")

    if st.button("🔁 Main Lagi"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.experimental_rerun()
