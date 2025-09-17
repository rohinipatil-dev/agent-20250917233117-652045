import streamlit as st
from openai import OpenAI

# --------------- App Config ---------------
st.set_page_config(page_title="Guru Informatika SMA - Kurikulum Merdeka (AI)", page_icon="🧑‍🏫", layout="wide")

# --------------- Helpers ---------------
def get_phase(grade: str) -> str:
    if grade == "X (10)":
        return "Fase E"
    return "Fase F"

def build_system_prompt(language: str, grade: str, area: str, mode: str, difficulty: str) -> str:
    phase = get_phase(grade)
    if language == "Bahasa Indonesia":
        return (
            "Anda adalah Guru Informatika profesional untuk jenjang SMA/MA di Indonesia yang mengajar dengan Kurikulum Merdeka. "
            f"Fokus: {area}. Kelas: {grade} ({phase}). "
            "Peran Anda: perencana pembelajaran, fasilitator PBL, dan evaluator yang berorientasi pada Capaian Pembelajaran (CP) dan Tujuan Pembelajaran/ATP. "
            "Gaya komunikasi: ramah, jelas, ringkas, dan terstruktur; gunakan bahasa Indonesia baku yang mudah dipahami siswa SMA. "
            "Prinsip pedagogi: diferensiasi (konten, proses, produk), berpusat pada siswa, literasi-numerasi, TPACK, integrasi Profil Pelajar Pancasila, dan etika digital. "
            f"Mode saat ini: {mode}. Tingkat kedalaman: {difficulty}. "
            "Gunakan poin/bullet dan tabel bila relevan. Sertakan contoh kontekstual Indonesia dan proyek berbasis masalah nyata. "
            "Jika diminta kode, prioritaskan Python atau pseudocode yang mudah dipahami pemula, dengan penjelasan langkah per langkah. "
            "Referensikan praktik Kurikulum Merdeka (CP, TP/ATP) secara wajar; hindari mengarang regulasi spesifik. "
            "Cegah plagiarisme; jika mencontoh sumber, parafrase dan cantumkan rujukan secara ringkas."
        )
    else:
        return (
            "You are a professional Informatics teacher for Indonesian senior high school (SMA/MA) implementing the Kurikulum Merdeka. "
            f"Focus: {area}. Grade: {grade} ({phase}). "
            "Your roles: learning designer, PBL facilitator, and evaluator aligned to Indonesia's CP (Learning Outcomes) and TP/ATP. "
            "Style: friendly, clear, concise, and structured; respond in English unless the user uses Indonesian. "
            f"Current mode: {mode}. Depth: {difficulty}. "
            "Use bullets and tables where helpful. Include authentic, local Indonesian contexts and problem-based projects. "
            "When code is requested, prefer beginner-friendly Python or pseudocode with step-by-step explanations. "
            "Reference Kurikulum Merdeka practices sensibly; avoid fabricating regulations. "
            "Prevent plagiarism; paraphrase and cite sources briefly when applicable."
        )

def build_mode_scaffold(language: str, grade: str, area: str, mode: str) -> str:
    phase = get_phase(grade)
    if language == "Bahasa Indonesia":
        if mode == "Rancang Modul Ajar":
            return (
                "Tugas: Rancang Modul Ajar Informatika sesuai Kurikulum Merdeka.\n"
                f"Konteks: Kelas {grade} ({phase}), Topik: {area}.\n"
                "Struktur keluaran yang diharapkan:\n"
                "- Rasional singkat & Prasyarat/Kompetensi awal\n"
                "- Capaian Pembelajaran (CP) terkait (ringkas, tidak mengada-ada)\n"
                "- Tujuan Pembelajaran & Indikator Keberhasilan (SMART)\n"
                "- Alur Tujuan Pembelajaran (ATP) ringkas yang relevan\n"
                "- Materi esensial & Miskonsepsi umum\n"
                "- Skenario Pembelajaran (Pendahuluan–Inti–Penutup) dengan alokasi waktu\n"
                "- Strategi diferensiasi (konten/proses/produk)\n"
                "- Integrasi Profil Pelajar Pancasila & literasi-numerasi\n"
                "- Media/Alat/Sumber belajar (termasuk TI/TPACK)\n"
                "- Asesmen: Diagnostik, Formatif, Sumatif + kisi-kisi & rubrik\n"
                "- Keamanan & Etika digital terkait topik\n"
                "- Rencana remedial & pengayaan\n"
                "- LKPD/aktivitas siswa (ringkas, langkah-langkah jelas)\n"
                "- Referensi/sumber rujukan\n"
                "Tambahkan contoh lokal Indonesia dan jika relevan sertakan contoh kode (Python/pseudocode) disertai penjelasan."
            )
        elif mode == "Rancang Penilaian":
            return (
                "Tugas: Rancang instrumen penilaian Informatika.\n"
                f"Konteks: Kelas {grade} ({phase}), Topik: {area}.\n"
                "Sertakan:\n"
                "- Tujuan penilaian dan indikator ketercapaian\n"
                "- Blueprint/kisi-kisi (level kognitif, kompetensi, bobot)\n"
                "- Soal formatif dan sumatif (variasi: PG, isian, esai, praktikum/proyek)\n"
                "- Kunci jawaban dan rubrik penskoran jelas\n"
                "- Kriteria ketuntasan dan umpan balik contoh\n"
                "- Strategi AKM-like dan asesmen autentik berbasis proyek\n"
                "- Diferensiasi penilaian dan akomodasi"
            )
        elif mode == "Buat Soal & Kunci":
            return (
                "Tugas: Buat bank soal Informatika beserta kunci.\n"
                f"Konteks: Kelas {grade} ({phase}), Topik: {area}.\n"
                "Sertakan minimal:\n"
                "- 8 soal pilihan ganda (bertingkat kognitif beragam) + kunci + alasan\n"
                "- 3 soal isian/singkat + kunci\n"
                "- 2 soal esai + rubrik penskoran\n"
                "- 1 tugas praktikum/proyek singkat + rubrik\n"
                "Gunakan konteks Indonesia dan hindari pertanyaan ambigu."
            )
        elif mode == "Bantu Proyek/PBL":
            return (
                "Tugas: Rancang proyek/PBL Informatika.\n"
                f"Konteks: Kelas {grade} ({phase}), Topik: {area}.\n"
                "Sertakan:\n"
                "- Tema proyek dan Driving Question\n"
                "- Tujuan pembelajaran & luaran (deliverables)\n"
                "- Langkah kerja bertahap (milestone & timeline)\n"
                "- Sumber daya/alat yang dibutuhkan\n"
                "- Kriteria keberhasilan & rubrik\n"
                "- Diferensiasi dan peran tim\n"
                "- Strategi keamanan & etika digital terkait\n"
                "- Ide pameran/presentasi produk dan refleksi"
            )
        else:
            return (
                "Tugas: Bimbingan belajar Informatika untuk siswa SMA.\n"
                f"Fokus: {area}, Kelas {grade} ({phase}). "
                "Jawab pertanyaan dengan contoh konkret, analogi sederhana, dan latihan singkat jika relevan."
            )
    else:
        if mode == "Rancang Modul Ajar":
            return (
                "Task: Design a Lesson Module aligned with Indonesia's Kurikulum Merdeka.\n"
                f"Context: Grade {grade} ({phase}), Topic: {area}.\n"
                "Provide: rationale, prior knowledge, concise CP mapping, learning objectives & indicators, brief ATP, essential content & misconceptions, lesson flow (intro-core-closing) with timing, differentiation, Pancasila Profile integration, media/TPACK, diagnostic/formative/summative assessment with rubrics, digital ethics, remedial/enrichment, student worksheets/activities, references. Use Indonesian context; include sample code (Python/pseudocode) when relevant."
            )
        elif mode == "Rancang Penilaian":
            return (
                "Task: Design Informatics assessments.\n"
                f"Context: Grade {grade} ({phase}), Topic: {area}.\n"
                "Include objectives, indicators, blueprint, formative and summative items, answer keys and rubrics, mastery criteria, feedback samples, authentic and differentiated assessment."
            )
        elif mode == "Buat Soal & Kunci":
            return (
                "Task: Create an Informatics question bank with keys.\n"
                f"Context: Grade {grade} ({phase}), Topic: {area}.\n"
                "Provide at least 8 MCQs (with rationales), 3 short-answer items, 2 essays (with rubrics), and 1 short practical/project task (with rubric)."
            )
        elif mode == "Bantu Proyek/PBL":
            return (
                "Task: Design a PBL project.\n"
                f"Context: Grade {grade} ({phase}), Topic: {area}.\n"
                "Include driving question, learning goals, deliverables, milestones/timeline, resources, success criteria & rubrics, team roles, digital ethics, and showcase/reflection ideas."
            )
        else:
            return (
                "Task: Tutor Informatics for Indonesian high-school students.\n"
                f"Focus: {area}, Grade {grade} ({phase}). "
                "Answer with concrete examples, simple analogies, and short practice when relevant."
            )

def build_user_message(user_input: str, language: str, grade: str, area: str, mode: str, difficulty: str) -> str:
    scaffold = build_mode_scaffold(language, grade, area, mode)
    guidance = ""
    if language == "Bahasa Indonesia":
        guidance = (
            f"\nKedalaman materi: {difficulty}."
            "\nGunakan format yang rapi, dengan judul-bagian yang jelas. Jika membuat tabel, gunakan Markdown."
            "\nJika topik kontroversial atau belum pasti, jelaskan keterbatasan secara jujur."
        )
    else:
        guidance = (
            f"\nDepth: {difficulty}."
            "\nUse clean structure with clear section headings. Use Markdown for tables."
            "\nIf content is uncertain, state limitations honestly."
        )
    prompt = f"{scaffold}\n\nInstruksi tambahan pengguna:\n{user_input.strip()}\n{guidance}"
    return prompt

def init_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "config_sig" not in st.session_state:
        st.session_state.config_sig = ""

def config_signature(model: str, language: str, grade: str, area: str, mode: str, difficulty: str) -> str:
    return "|".join([model, language, grade, area, mode, difficulty])

def reset_conversation(system_prompt: str):
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

def ensure_system_prompt(system_prompt: str):
    if not st.session_state.messages or st.session_state.messages[0].get("role") != "system":
        reset_conversation(system_prompt)
    else:
        st.session_state.messages[0]["content"] = system_prompt

def chat_completion(client: OpenAI, model: str, messages):
    try:
        response = client.chat.completions.create(
            model=model,  # "gpt-3.5-turbo" or "gpt-4"
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Terjadi kesalahan saat memanggil model: {e}"

def downloadable_text():
    # Concatenate last assistant message for download
    for msg in reversed(st.session_state.messages):
        if msg["role"] == "assistant":
            return msg["content"]
    return ""

# --------------- Sidebar ---------------
st.sidebar.title("Pengaturan")
model = st.sidebar.selectbox("Model", options=["gpt-4", "gpt-3.5-turbo"], index=0)
language = st.sidebar.selectbox("Bahasa / Language", options=["Bahasa Indonesia", "English"], index=0)
grade = st.sidebar.selectbox("Kelas", options=["X (10)", "XI (11)", "XII (12)"], index=0)
area = st.sidebar.selectbox(
    "Fokus Materi",
    options=[
        "Algoritma & Pemrograman",
        "Data & Analitika",
        "Jaringan & Internet",
        "Sistem Komputer",
        "Keamanan Siber",
        "Kecerdasan Buatan Dasar",
        "Dampak Sosial & Etika Digital",
        "Desain & Pengembangan Aplikasi",
        "Pemodelan & Simulasi",
    ],
    index=0
)
mode = st.sidebar.selectbox(
    "Mode",
    options=["Chat Bimbingan", "Rancang Modul Ajar", "Rancang Penilaian", "Buat Soal & Kunci", "Bantu Proyek/PBL"],
    index=0
)
difficulty = st.sidebar.select_slider("Kedalaman Materi", options=["Dasar", "Menengah", "Lanjut"], value="Menengah")
st.sidebar.divider()
clear = st.sidebar.button("🔄 Mulai Ulang Percakapan", use_container_width=True)

# --------------- Initialize ---------------
init_state()
client = OpenAI()

system_prompt = build_system_prompt(language, grade, area, mode, difficulty)
sig = config_signature(model, language, grade, area, mode, difficulty)

if clear or st.session_state.config_sig != sig:
    reset_conversation(system_prompt)
    st.session_state.config_sig = sig
else:
    ensure_system_prompt(system_prompt)

# --------------- Header ---------------
st.title("🧑‍🏫 Guru Informatika SMA - Kurikulum Merdeka (AI)")
phase_label = get_phase(grade)
st.caption(f"Mode: {mode} • Kelas: {grade} ({phase_label}) • Fokus: {area} • Model: {model}")

# --------------- Presets / Tips ---------------
with st.expander("Contoh permintaan (klik untuk menyalin)", expanded=False):
    if language == "Bahasa Indonesia":
        st.code(
            "- Buat modul ajar 'Pengenalan Algoritma dan Flowchart' untuk 2 x 45 menit.\n"
            "- Rancang 10 soal PG tentang jaringan komputer dasar dengan kunci dan alasan.\n"
            "- Susun proyek PBL: Aplikasi kalkulator sederhana berbasis Python untuk siswa kelas X.\n"
            "- Minta penjelasan sederhana tentang variabel, tipe data, dan operator (dengan latihan).",
            language="text",
        )
    else:
        st.code(
            "- Create a lesson module on 'Introduction to Algorithms and Flowcharts' for 2 x 45 minutes.\n"
            "- Design 10 MCQs on basic computer networks with keys and rationales.\n"
            "- Plan a PBL project: Simple Python calculator app for Grade 10.\n"
            "- Explain variables, data types, and operators with short practice.",
            language="text",
        )

# --------------- Chat History ---------------
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --------------- Input ---------------
placeholder_text = "Tulis pertanyaan atau instruksi Anda di sini..." if language == "Bahasa Indonesia" else "Type your question or instructions here..."
user_input = st.chat_input(placeholder=placeholder_text)

if user_input:
    # Build user message with scaffold according to mode
    full_user_prompt = build_user_message(user_input, language, grade, area, mode, difficulty)
    st.session_state.messages.append({"role": "user", "content": full_user_prompt})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Menyusun jawaban..."):
            reply = chat_completion(client, model, st.session_state.messages)
            st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

# --------------- Download Output ---------------
st.divider()
dl_text = downloadable_text()
if dl_text:
    st.download_button(
        label="⬇️ Unduh Hasil Terakhir (Markdown)",
        data=dl_text,
        file_name="hasil_guru_informatika.md",
        mime="text/markdown",
        use_container_width=True,
    )

# --------------- Footer ---------------
st.caption(
    "Catatan: Aplikasi ini menggunakan model OpenAI melalui antarmuka chat. Pastikan Anda telah mengatur variabel lingkungan OPENAI_API_KEY sebelum menjalankan aplikasi."
)