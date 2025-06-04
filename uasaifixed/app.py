from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__, static_folder='static', template_folder='templates')

# Knowledge Base: Database resep yang sangat diperluas dengan lebih banyak variasi
recipes_db = [
    # ===== RESEP DENGAN TELUR AYAM BANYAK =====
    {
        "name": "Nasi goreng telur ayam spesial",
        "ingredients": ["nasi_putih", "telur_ayam_banyak", "bawang_merah", "kecap_manis", "garam", "minyak_goreng", "cabai"],
        "description": "Nasi goreng dengan telur ayam yang banyak (>3 butir), bawang merah, dan cabai pedas."
    },
    {
        "name": "Omelet telur ayam jumbo",
        "ingredients": ["telur_ayam_banyak", "sayur_hijau", "garam", "minyak_goreng", "bawang_merah", "keju"],
        "description": "Omelet besar dengan banyak telur ayam dan isi sayuran hijau serta keju."
    },
    {
        "name": "Telur balado pedas",
        "ingredients": ["telur_ayam_banyak", "cabai_banyak", "bawang_merah", "tomat", "garam", "minyak_goreng"],
        "description": "Telur ayam yang dimasak dengan sambal balado pedas menggunakan banyak cabai."
    },
    {
        "name": "Scrambled eggs deluxe",
        "ingredients": ["telur_ayam_banyak", "susu", "mentega", "garam", "lada_hitam", "keju"],
        "description": "Telur orak-arik mewah dengan susu, mentega, dan keju."
    },
    
    # ===== RESEP DENGAN TELUR AYAM SEDIKIT =====
    {
        "name": "Telur dadar sederhana",
        "ingredients": ["telur_ayam_sedikit", "kecap_manis", "garam", "minyak_goreng"],
        "description": "Telur dadar sederhana dengan kecap manis untuk 1-3 butir telur."
    },
    {
        "name": "Telur ceplok kecap",
        "ingredients": ["telur_ayam_sedikit", "kecap_manis", "bawang_merah", "garam", "minyak_goreng"],
        "description": "Telur ceplok dengan siraman kecap manis dan bawang merah."
    },
    {
        "name": "Nasi telur ceplok",
        "ingredients": ["nasi_putih", "telur_ayam_sedikit", "kecap_manis", "garam", "minyak_goreng"],
        "description": "Nasi putih dengan telur ceplok dan kecap manis."
    },
    
    # ===== RESEP DENGAN TELUR BEBEK =====
    {
        "name": "Orak-arik telur bebek spesial",
        "ingredients": ["telur_bebek_banyak", "bawang_merah", "cabai", "garam", "minyak_goreng"],
        "description": "Orak-arik telur bebek yang gurih dengan bawang merah dan cabai."
    },
    {
        "name": "Telur bebek balado",
        "ingredients": ["telur_bebek_sedikit", "cabai_banyak", "bawang_merah", "tomat", "garam"],
        "description": "Telur bebek dengan sambal balado yang pedas."
    },
    {
        "name": "Nasi goreng telur bebek",
        "ingredients": ["nasi_putih", "telur_bebek_banyak", "bawang_bombay", "kecap_asin", "garam", "minyak_goreng"],
        "description": "Nasi goreng istimewa dengan telur bebek dan bawang bombay."
    },
    
    # ===== RESEP DENGAN DAGING AYAM BANYAK =====
    {
        "name": "Ayam goreng tepung crispy",
        "ingredients": ["daging_ayam_banyak", "tepung_terigu", "garam", "minyak_goreng_banyak", "bawang_putih"],
        "description": "Ayam goreng dengan tepung yang crispy menggunakan daging ayam yang banyak (>500g)."
    },
    {
        "name": "Sup ayam sayuran lengkap",
        "ingredients": ["daging_ayam_banyak", "sayur_hijau", "wortel", "bawang_bombay", "garam", "air_bersih"],
        "description": "Sup ayam yang kaya dengan banyak daging dan sayuran."
    },
    {
        "name": "Ayam kecap manis jumbo",
        "ingredients": ["daging_ayam_banyak", "kecap_manis", "bawang_merah", "jahe", "garam", "minyak_goreng"],
        "description": "Ayam kecap manis dengan porsi daging yang banyak."
    },
    {
        "name": "Ayam bakar bumbu lengkap",
        "ingredients": ["daging_ayam_banyak", "kecap_manis", "bawang_merah", "bawang_putih", "jahe", "kunyit", "garam"],
        "description": "Ayam bakar dengan bumbu lengkap dan daging yang banyak."
    },
    
    # ===== RESEP DENGAN DAGING AYAM SEDIKIT =====
    {
        "name": "Tumis ayam sederhana",
        "ingredients": ["daging_ayam_sedikit", "bawang_merah", "kecap_manis", "garam", "minyak_goreng"],
        "description": "Tumis ayam sederhana dengan daging sedikit (≤500g)."
    },
    {
        "name": "Ayam suwir sambal",
        "ingredients": ["daging_ayam_sedikit", "cabai", "bawang_merah", "garam", "minyak_goreng"],
        "description": "Ayam suwir dengan sambal untuk daging ayam yang sedikit."
    },
    
    # ===== RESEP DENGAN DAGING SAPI BERTULANG =====
    {
        "name": "Sop buntut sapi",
        "ingredients": ["daging_sapi_tulang", "wortel", "kentang", "bawang_bombay", "garam", "air_bersih"],
        "description": "Sop buntut sapi dengan sayuran dan kentang menggunakan daging bertulang."
    },
    {
        "name": "Rawon sapi sederhana",
        "ingredients": ["daging_sapi_tulang", "kluwek", "bawang_merah", "bawang_putih", "jahe", "garam"],
        "description": "Rawon sapi dengan daging bertulang dan bumbu kluwek."
    },
    {
        "name": "Gulai sapi tulang",
        "ingredients": ["daging_sapi_tulang", "santan", "cabai", "bawang_merah", "jahe", "kunyit", "garam"],
        "description": "Gulai sapi dengan tulang dan santan yang gurih."
    },
    
    # ===== RESEP DENGAN DAGING SAPI TANPA TULANG =====
    {
        "name": "Rendang sapi sederhana",
        "ingredients": ["daging_sapi_tanpa_tulang", "santan", "cabai", "bawang_merah", "jahe", "garam"],
        "description": "Rendang sapi dengan daging tanpa tulang dan santan."
    },
    {
        "name": "Daging sapi lada hitam",
        "ingredients": ["daging_sapi_tanpa_tulang", "lada_hitam", "bawang_bombay", "kecap_manis", "garam", "minyak_goreng"],
        "description": "Daging sapi tanpa tulang dengan lada hitam dan kecap manis."
    },
    {
        "name": "Semur daging sapi",
        "ingredients": ["daging_sapi_tanpa_tulang", "kecap_manis", "bawang_merah", "bawang_putih", "garam", "air_bersih"],
        "description": "Semur daging sapi tanpa tulang dengan kecap manis."
    },
    
    # ===== RESEP DENGAN BUMBU DASAR =====
    {
        "name": "Sambal terasi pedas",
        "ingredients": ["cabai_banyak", "terasi", "bawang_merah", "tomat", "garam"],
        "description": "Sambal terasi yang sangat pedas dengan banyak cabai."
    },
    {
        "name": "Tumis bawang cabai",
        "ingredients": ["bawang_merah", "cabai_sedikit", "garam", "minyak_goreng"],
        "description": "Tumis bawang merah dengan cabai sedikit untuk yang tidak suka pedas."
    },
    {
        "name": "Kecap manis bawang",
        "ingredients": ["kecap_manis", "bawang_merah", "cabai_sedikit", "garam"],
        "description": "Saus kecap manis dengan bawang merah dan cabai."
    },
    
    # ===== RESEP DENGAN IKAN BESAR =====
    {
        "name": "Ikan bakar bumbu lengkap",
        "ingredients": ["ikan_besar", "kecap_manis", "bawang_merah", "cabai", "jahe", "kunyit", "garam"],
        "description": "Ikan besar yang dibakar dengan bumbu lengkap dan rempah-rempah."
    },
    {
        "name": "Gulai ikan besar",
        "ingredients": ["ikan_besar", "santan", "cabai", "bawang_merah", "jahe", "kunyit", "garam"],
        "description": "Gulai ikan dengan ikan besar dan santan yang kental."
    },
    {
        "name": "Ikan asam manis jumbo",
        "ingredients": ["ikan_besar", "tomat", "bawang_bombay", "gula", "cuka", "minyak_goreng"],
        "description": "Ikan besar dengan saus asam manis yang segar."
    },
    
    # ===== RESEP DENGAN IKAN KECIL =====
    {
        "name": "Ikan goreng sambal",
        "ingredients": ["ikan_kecil", "cabai", "tomat", "bawang_merah", "garam", "minyak_goreng"],
        "description": "Ikan kecil yang digoreng dengan sambal tomat dan cabai."
    },
    {
        "name": "Pepes ikan kecil",
        "ingredients": ["ikan_kecil", "bawang_merah", "cabai", "tomat", "garam", "daun_pisang"],
        "description": "Ikan kecil yang dibungkus daun pisang dan dikukus dengan bumbu."
    },
    
    # ===== RESEP DENGAN IKAN TERI =====
    {
        "name": "Nasi goreng teri",
        "ingredients": ["nasi_putih", "ikan_teri", "bawang_merah", "cabai", "garam", "minyak_goreng"],
        "description": "Nasi goreng dengan ikan teri yang gurih dan cabai."
    },
    {
        "name": "Sambal teri kentang",
        "ingredients": ["ikan_teri", "kentang", "cabai_banyak", "bawang_merah", "garam", "minyak_goreng"],
        "description": "Sambal teri dengan kentang yang pedas dan gurih."
    },
    {
        "name": "Tumis teri kacang",
        "ingredients": ["ikan_teri", "kacang_tanah", "cabai", "bawang_merah", "garam", "minyak_goreng"],
        "description": "Tumis ikan teri dengan kacang tanah yang renyah."
    },
    
    # ===== RESEP DENGAN NASI BANYAK =====
    {
        "name": "Nasi goreng spesial jumbo",
        "ingredients": ["nasi_putih_banyak", "telur_ayam_banyak", "daging_ayam_sedikit", "bawang_merah", "kecap_manis", "garam"],
        "description": "Nasi goreng jumbo dengan nasi yang banyak dan berbagai topping."
    },
    {
        "name": "Nasi kuning besar",
        "ingredients": ["nasi_putih_banyak", "kunyit", "santan", "bawang_merah", "jahe", "garam"],
        "description": "Nasi kuning dengan porsi besar menggunakan kunyit dan santan."
    },
    
    # ===== RESEP DENGAN NASI SEDIKIT =====
    {
        "name": "Nasi goreng sederhana",
        "ingredients": ["nasi_putih_sedikit", "bawang_merah", "kecap_manis", "garam", "minyak_goreng"],
        "description": "Nasi goreng sederhana dengan nasi yang sedikit."
    },
    {
        "name": "Nasi kecap bawang",
        "ingredients": ["nasi_putih_sedikit", "kecap_manis", "bawang_bombay", "garam", "minyak_goreng"],
        "description": "Nasi dengan kecap manis dan bawang bombay."
    },
    
    # ===== RESEP DENGAN MIE INSTAN BANYAK =====
    {
        "name": "Mie goreng jumbo",
        "ingredients": ["mie_instan_banyak", "telur_ayam_sedikit", "sayur_hijau", "bawang_merah", "kecap_manis"],
        "description": "Mie goreng jumbo dengan banyak mie instan dan topping lengkap."
    },
    {
        "name": "Mie kuah spesial",
        "ingredients": ["mie_instan_banyak", "daging_ayam_sedikit", "sayur_hijau", "bawang_merah", "garam", "air_bersih"],
        "description": "Mie kuah spesial dengan banyak mie dan topping daging."
    },
    
    # ===== RESEP DENGAN MIE INSTAN SEDIKIT =====
    {
        "name": "Mie goreng sederhana",
        "ingredients": ["mie_instan_sedikit", "bawang_merah", "kecap_manis", "garam", "minyak_goreng"],
        "description": "Mie goreng sederhana dengan mie instan yang sedikit."
    },
    {
        "name": "Mie kuah telur",
        "ingredients": ["mie_instan_sedikit", "telur_ayam_sedikit", "bawang_merah", "garam", "air_bersih"],
        "description": "Mie kuah dengan telur dan mie instan yang sedikit."
    },
    
    # ===== RESEP DENGAN SAYURAN HIJAU BANYAK =====
    {
        "name": "Capcay sayuran lengkap",
        "ingredients": ["sayur_hijau_banyak", "wortel", "kembang_kol", "bawang_putih", "garam", "minyak_goreng"],
        "description": "Capcay dengan banyak sayuran hijau dan berbagai macam sayuran lain."
    },
    {
        "name": "Tumis kangkung spesial",
        "ingredients": ["sayur_hijau_banyak", "terasi", "cabai", "bawang_merah", "garam", "minyak_goreng"],
        "description": "Tumis kangkung dengan banyak sayuran hijau dan terasi."
    },
    {
        "name": "Sayur sop lengkap",
        "ingredients": ["sayur_hijau_banyak", "wortel", "kentang", "bawang_bombay", "garam", "air_bersih"],
        "description": "Sayur sop dengan banyak sayuran hijau dan sayuran lainnya."
    },
    
    # ===== RESEP DENGAN SAYURAN HIJAU SEDIKIT =====
    {
        "name": "Tumis sayur sederhana",
        "ingredients": ["sayur_hijau_sedikit", "bawang_putih", "garam", "minyak_goreng"],
        "description": "Tumis sayuran hijau sederhana dengan bawang putih."
    },
    {
        "name": "Sayur bening",
        "ingredients": ["sayur_hijau_sedikit", "jagung", "garam", "air_bersih"],
        "description": "Sayur bening dengan sayuran hijau sedikit dan jagung."
    },
    
    # ===== RESEP DENGAN CABAI BANYAK =====
    {
        "name": "Ayam geprek super pedas",
        "ingredients": ["daging_ayam_sedikit", "cabai_banyak", "bawang_putih", "garam", "minyak_goreng"],
        "description": "Ayam geprek dengan sambal yang sangat pedas."
    },
    {
        "name": "Tumis kangkung pedas",
        "ingredients": ["sayur_hijau_sedikit", "cabai_banyak", "terasi", "bawang_merah", "garam"],
        "description": "Tumis kangkung dengan level kepedasan tinggi."
    },
    
    # ===== RESEP DENGAN CABAI SEDIKIT =====
    {
        "name": "Telur dadar cabai",
        "ingredients": ["telur_ayam_sedikit", "cabai_sedikit", "bawang_merah", "garam", "minyak_goreng"],
        "description": "Telur dadar dengan sedikit cabai untuk rasa yang mild."
    },
    
    # ===== RESEP DENGAN MINYAK GORENG BANYAK =====
    {
        "name": "Ayam goreng crispy",
        "ingredients": ["daging_ayam_banyak", "tepung_terigu", "garam", "minyak_goreng_banyak"],
        "description": "Ayam goreng yang crispy dengan deep frying menggunakan banyak minyak."
    },
    {
        "name": "Kentang goreng crispy",
        "ingredients": ["kentang", "garam", "minyak_goreng_banyak"],
        "description": "Kentang goreng yang crispy dengan deep frying."
    },
    {
        "name": "Tahu goreng crispy",
        "ingredients": ["tahu", "tepung_terigu", "garam", "minyak_goreng_banyak"],
        "description": "Tahu goreng yang crispy dengan banyak minyak."
    },
    
    # ===== RESEP DENGAN MINYAK GORENG SEDIKIT =====
    {
        "name": "Tumis sederhana",
        "ingredients": ["bawang_merah", "garam", "minyak_goreng_sedikit"],
        "description": "Tumis sederhana dengan minyak goreng yang sedikit."
    },
    {
        "name": "Telur dadar tipis",
        "ingredients": ["telur_ayam_sedikit", "garam", "minyak_goreng_sedikit"],
        "description": "Telur dadar tipis dengan minyak yang sedikit."
    },
    
    # ===== RESEP TAMBAHAN UNTUK VARIASI =====
    {
        "name": "Gado-gado sederhana",
        "ingredients": ["sayur_hijau_banyak", "tahu", "tempe", "kacang_tanah", "cabai_sedikit", "gula_merah"],
        "description": "Gado-gado dengan sayuran, tahu, tempe, dan bumbu kacang."
    },
    {
        "name": "Soto ayam sederhana",
        "ingredients": ["daging_ayam_sedikit", "kunyit", "jahe", "bawang_merah", "garam", "air_bersih"],
        "description": "Soto ayam dengan bumbu sederhana dan kunyit."
    },
    {
        "name": "Bakwan sayur",
        "ingredients": ["sayur_hijau_sedikit", "tepung_terigu", "garam", "minyak_goreng_banyak", "bawang_merah"],
        "description": "Bakwan sayur yang digoreng dengan tepung terigu."
    },
    {
        "name": "Es teh manis",
        "ingredients": ["teh", "gula", "air_bersih"],
        "description": "Minuman es teh manis yang segar."
    },
    {
        "name": "Jus wortel segar",
        "ingredients": ["wortel", "gula", "air_bersih"],
        "description": "Jus wortel segar dengan gula."
    },
    {
        "name": "Wedang jahe hangat",
        "ingredients": ["jahe", "gula_merah", "air_bersih"],
        "description": "Minuman jahe hangat dengan gula merah."
    }
]

# Struktur pertanyaan yang diatur ulang sesuai permintaan:
# Telur → Daging → Nasi → Garam → Kecap → Minyak → Sayuran → Bawang → dst
question_flow = [
    # ===== KATEGORI TELUR - PERTANYAAN UTAMA =====
    {
        "id": "telur_main",
        "question": "Apakah Anda memiliki telur di rumah?",
        "yes_next": "telur_jenis_ayam",
        "no_next": "daging_main",
        "ingredient": None
    },
    
    # ===== SUB-KATEGORI TELUR AYAM =====
    {
        "id": "telur_jenis_ayam",
        "question": "Apakah telur yang Anda miliki adalah telur ayam?",
        "yes_next": "telur_ayam_jumlah",
        "no_next": "telur_jenis_bebek",
        "ingredient": None
    },
    {
        "id": "telur_ayam_jumlah",
        "question": "Apakah telur ayam yang Anda miliki lebih dari 3 butir?",
        "yes_next": "telur_bebek_check",
        "no_next": "telur_bebek_check",
        "yes_ingredient": "telur_ayam_banyak",
        "no_ingredient": "telur_ayam_sedikit"
    },
    
    # ===== SUB-KATEGORI TELUR BEBEK =====
    {
        "id": "telur_jenis_bebek",
        "question": "Apakah telur yang Anda miliki adalah telur bebek?",
        "yes_next": "telur_bebek_jumlah",
        "no_next": "daging_main",
        "ingredient": None
    },
    {
        "id": "telur_bebek_jumlah",
        "question": "Apakah telur bebek yang Anda miliki lebih dari 3 butir?",
        "yes_next": "daging_main",
        "no_next": "daging_main",
        "yes_ingredient": "telur_bebek_banyak",
        "no_ingredient": "telur_bebek_sedikit"
    },
    {
        "id": "telur_bebek_check",
        "question": "Selain telur ayam, apakah Anda juga memiliki telur bebek?",
        "yes_next": "telur_bebek_jumlah",
        "no_next": "daging_main",
        "ingredient": None
    },
    
    # ===== KATEGORI DAGING - PERTANYAAN UTAMA =====
    {
        "id": "daging_main",
        "question": "Apakah Anda memiliki daging di rumah?",
        "yes_next": "daging_jenis_ayam",
        "no_next": "nasi_main",  # Langsung ke nasi jika tidak ada daging
        "ingredient": None
    },
    
    # ===== SUB-KATEGORI DAGING AYAM =====
    {
        "id": "daging_jenis_ayam",
        "question": "Apakah daging yang Anda miliki adalah daging ayam?",
        "yes_next": "daging_ayam_jumlah",
        "no_next": "daging_jenis_sapi",
        "ingredient": None
    },
    {
        "id": "daging_ayam_jumlah",
        "question": "Apakah daging ayam yang Anda miliki lebih dari 500 gram?",
        "yes_next": "daging_sapi_check",
        "no_next": "daging_sapi_check",
        "yes_ingredient": "daging_ayam_banyak",
        "no_ingredient": "daging_ayam_sedikit"
    },
    
    # ===== SUB-KATEGORI DAGING SAPI =====
    {
        "id": "daging_jenis_sapi",
        "question": "Apakah daging yang Anda miliki adalah daging sapi?",
        "yes_next": "daging_sapi_tulang",
        "no_next": "nasi_main",  # Langsung ke nasi jika bukan ayam/sapi
        "ingredient": None
    },
    {
        "id": "daging_sapi_tulang",
        "question": "Apakah daging sapi yang Anda miliki termasuk bagian yang ada tulangnya (seperti buntut, iga)?",
        "yes_next": "nasi_main",  # Ke nasi setelah daging
        "no_next": "nasi_main",  # Ke nasi setelah daging
        "yes_ingredient": "daging_sapi_tulang",
        "no_ingredient": "daging_sapi_tanpa_tulang"
    },
    {
        "id": "daging_sapi_check",
        "question": "Selain daging ayam, apakah Anda juga memiliki daging sapi?",
        "yes_next": "daging_sapi_tulang",
        "no_next": "nasi_main",  # Ke nasi setelah daging
        "ingredient": None
    },
    
    # ===== KATEGORI NASI/BERAS - SETELAH DAGING =====
    {
        "id": "nasi_main",
        "question": "Apakah Anda memiliki nasi putih yang sudah matang di rumah?",
        "yes_next": "nasi_jumlah",
        "no_next": "beras_check",
        "ingredient": None
    },
    
    # ===== SUB-KATEGORI NASI BERDASARKAN JUMLAH =====
    {
        "id": "nasi_jumlah",
        "question": "Apakah nasi putih yang Anda miliki cukup untuk lebih dari 3 porsi?",
        "yes_next": "garam_main",  # Ke garam setelah nasi
        "no_next": "garam_main",  # Ke garam setelah nasi
        "yes_ingredient": "nasi_putih_banyak",
        "no_ingredient": "nasi_putih_sedikit"
    },
    {
        "id": "beras_check",
        "question": "Apakah Anda memiliki beras mentah yang bisa dimasak?",
        "yes_next": "garam_main",  # Ke garam setelah nasi/beras
        "no_next": "garam_main",  # Ke garam setelah nasi/beras
        "yes_ingredient": "beras",
        "no_ingredient": None
    },
    
    # ===== KATEGORI GARAM - SETELAH NASI =====
    {
        "id": "garam_main",
        "question": "Apakah Anda memiliki garam di rumah?",
        "yes_next": "kecap_main",  # Ke kecap setelah garam
        "no_next": "kecap_main",  # Ke kecap setelah garam
        "yes_ingredient": "garam",
        "no_ingredient": None
    },
    
    # ===== KATEGORI KECAP - SETELAH GARAM =====
    {
        "id": "kecap_main",
        "question": "Apakah Anda memiliki kecap manis di rumah?",
        "yes_next": "kecap_asin_check",
        "no_next": "minyak_main",  # Ke minyak jika tidak ada kecap manis
        "yes_ingredient": "kecap_manis",
        "no_ingredient": None
    },
    {
        "id": "kecap_asin_check",
        "question": "Apakah Anda memiliki kecap asin di rumah?",
        "yes_next": "minyak_main",  # Ke minyak setelah kecap
        "no_next": "minyak_main",  # Ke minyak setelah kecap
        "yes_ingredient": "kecap_asin",
        "no_ingredient": None
    },
    
    # ===== KATEGORI MINYAK GORENG - SETELAH KECAP =====
    {
        "id": "minyak_main",
        "question": "Apakah Anda memiliki minyak goreng di rumah?",
        "yes_next": "minyak_jumlah",
        "no_next": "sayur_main",  # Ke sayuran jika tidak ada minyak
        "ingredient": None
    },
    
    # ===== SUB-KATEGORI MINYAK BERDASARKAN JUMLAH =====
    {
        "id": "minyak_jumlah",
        "question": "Apakah minyak goreng yang Anda miliki cukup banyak untuk menggoreng (lebih dari 500ml)?",
        "yes_next": "sayur_main",  # Ke sayuran setelah minyak
        "no_next": "sayur_main",  # Ke sayuran setelah minyak
        "yes_ingredient": "minyak_goreng_banyak",
        "no_ingredient": "minyak_goreng_sedikit"
    },
    
    # ===== KATEGORI SAYURAN HIJAU - SETELAH MINYAK =====
    {
        "id": "sayur_main",
        "question": "Apakah Anda memiliki sayuran hijau (seperti kangkung, bayam, sawi) di rumah?",
        "yes_next": "sayur_jumlah",
        "no_next": "wortel_check",
        "ingredient": None
    },
    
    # ===== SUB-KATEGORI SAYURAN HIJAU BERDASARKAN JUMLAH =====
    {
        "id": "sayur_jumlah",
        "question": "Apakah sayuran hijau yang Anda miliki cukup banyak (lebih dari 2 ikat)?",
        "yes_next": "wortel_check",
        "no_next": "wortel_check",
        "yes_ingredient": "sayur_hijau_banyak",
        "no_ingredient": "sayur_hijau_sedikit"
    },
    
    # ===== KATEGORI SAYURAN LAINNYA =====
    {
        "id": "wortel_check",
        "question": "Apakah Anda memiliki wortel di rumah?",
        "yes_next": "kentang_check",
        "no_next": "kentang_check",
        "yes_ingredient": "wortel",
        "no_ingredient": None
    },
    {
        "id": "kentang_check",
        "question": "Apakah Anda memiliki kentang di rumah?",
        "yes_next": "tomat_check",
        "no_next": "tomat_check",
        "yes_ingredient": "kentang",
        "no_ingredient": None
    },
    {
        "id": "tomat_check",
        "question": "Apakah Anda memiliki tomat di rumah?",
        "yes_next": "bawang_main",  # Ke bawang setelah sayuran
        "no_next": "bawang_main",  # Ke bawang setelah sayuran
        "yes_ingredient": "tomat",
        "no_ingredient": None
    },
    
    # ===== KATEGORI BAWANG - SETELAH SAYURAN =====
    {
        "id": "bawang_main",
        "question": "Apakah Anda memiliki bawang merah di rumah?",
        "yes_next": "bawang_putih_check",
        "no_next": "bawang_putih_check",
        "yes_ingredient": "bawang_merah",
        "no_ingredient": None
    },
    {
        "id": "bawang_putih_check",
        "question": "Apakah Anda memiliki bawang putih di rumah?",
        "yes_next": "bawang_bombay_check",
        "no_next": "bawang_bombay_check",
        "yes_ingredient": "bawang_putih",
        "no_ingredient": None
    },
    {
        "id": "bawang_bombay_check",
        "question": "Apakah Anda memiliki bawang bombay di rumah?",
        "yes_next": "cabai_main",  # Ke cabai setelah bawang
        "no_next": "cabai_main",  # Ke cabai setelah bawang
        "yes_ingredient": "bawang_bombay",
        "no_ingredient": None
    },
    
    # ===== KATEGORI CABAI - SETELAH BAWANG =====
    {
        "id": "cabai_main",
        "question": "Apakah Anda memiliki cabai di rumah?",
        "yes_next": "cabai_jumlah",
        "no_next": "ikan_main",  # Ke ikan jika tidak ada cabai
        "ingredient": None
    },
    
    # ===== SUB-KATEGORI CABAI BERDASARKAN JUMLAH =====
    {
        "id": "cabai_jumlah",
        "question": "Apakah cabai yang Anda miliki cukup banyak (lebih dari 10 buah atau suka makanan pedas)?",
        "yes_next": "ikan_main",  # Ke ikan setelah cabai
        "no_next": "ikan_main",  # Ke ikan setelah cabai
        "yes_ingredient": "cabai_banyak",
        "no_ingredient": "cabai_sedikit"
    },
    
    # ===== KATEGORI IKAN - SETELAH CABAI =====
    {
        "id": "ikan_main",
        "question": "Apakah Anda memiliki ikan di rumah?",
        "yes_next": "ikan_ukuran",
        "no_next": "mie_main",  # Ke mie jika tidak ada ikan
        "ingredient": None
    },
    
    # ===== SUB-KATEGORI IKAN BERDASARKAN UKURAN =====
    {
        "id": "ikan_ukuran",
        "question": "Apakah ikan yang Anda miliki berukuran besar (seperti kakap, gurame, nila besar)?",
        "yes_next": "ikan_teri_check",
        "no_next": "ikan_kecil_check",
        "yes_ingredient": "ikan_besar",
        "no_ingredient": None
    },
    {
        "id": "ikan_kecil_check",
        "question": "Apakah ikan yang Anda miliki berukuran kecil-sedang (seperti bandeng, kembung)?",
        "yes_next": "ikan_teri_check",
        "no_next": "ikan_teri_check",
        "yes_ingredient": "ikan_kecil",
        "no_ingredient": None
    },
    {
        "id": "ikan_teri_check",
        "question": "Apakah Anda memiliki ikan teri (ikan kering kecil)?",
        "yes_next": "mie_main",  # Ke mie setelah ikan
        "no_next": "mie_main",  # Ke mie setelah ikan
        "yes_ingredient": "ikan_teri",
        "no_ingredient": None
    },
    
    # ===== KATEGORI MIE - SETELAH IKAN =====
    {
        "id": "mie_main",
        "question": "Apakah Anda memiliki mie instan di rumah?",
        "yes_next": "mie_jumlah",
        "no_next": "tahu_tempe_main",  # Ke tahu/tempe jika tidak ada mie
        "ingredient": None
    },
    
    # ===== SUB-KATEGORI MIE BERDASARKAN JUMLAH =====
    {
        "id": "mie_jumlah",
        "question": "Apakah mie instan yang Anda miliki lebih dari 3 bungkus?",
        "yes_next": "tahu_tempe_main",  # Ke tahu/tempe setelah mie
        "no_next": "tahu_tempe_main",  # Ke tahu/tempe setelah mie
        "yes_ingredient": "mie_instan_banyak",
        "no_ingredient": "mie_instan_sedikit"
    },
    
    # ===== KATEGORI TAHU TEMPE =====
    {
        "id": "tahu_tempe_main",
        "question": "Apakah Anda memiliki tahu di rumah?",
        "yes_next": "tempe_check",
        "no_next": "tempe_check",
        "yes_ingredient": "tahu",
        "no_ingredient": None
    },
    {
        "id": "tempe_check",
        "question": "Apakah Anda memiliki tempe di rumah?",
        "yes_next": "bumbu_tambahan",  # Ke bumbu tambahan setelah tahu/tempe
        "no_next": "bumbu_tambahan",  # Ke bumbu tambahan setelah tahu/tempe
        "yes_ingredient": "tempe",
        "no_ingredient": None
    },
    
    # ===== KATEGORI BUMBU TAMBAHAN =====
    {
        "id": "bumbu_tambahan",
        "question": "Apakah Anda memiliki jahe di rumah?",
        "yes_next": "kunyit_check",
        "no_next": "kunyit_check",
        "yes_ingredient": "jahe",
        "no_ingredient": None
    },
    {
        "id": "kunyit_check",
        "question": "Apakah Anda memiliki kunyit di rumah?",
        "yes_next": "santan_check",
        "no_next": "santan_check",
        "yes_ingredient": "kunyit",
        "no_ingredient": None
    },
    {
        "id": "santan_check",
        "question": "Apakah Anda memiliki santan (kemasan atau kelapa parut) di rumah?",
        "yes_next": "tepung_check",
        "no_next": "tepung_check",
        "yes_ingredient": "santan",
        "no_ingredient": None
    },
    {
        "id": "tepung_check",
        "question": "Apakah Anda memiliki tepung terigu di rumah?",
        "yes_next": "gula_check",
        "no_next": "gula_check",
        "yes_ingredient": "tepung_terigu",
        "no_ingredient": None
    },
    {
        "id": "gula_check",
        "question": "Apakah Anda memiliki gula pasir di rumah?",
        "yes_next": "gula_merah_check",
        "no_next": "gula_merah_check",
        "yes_ingredient": "gula",
        "no_ingredient": None
    },
    {
        "id": "gula_merah_check",
        "question": "Apakah Anda memiliki gula merah atau gula jawa di rumah?",
        "yes_next": "bumbu_lanjutan",
        "no_next": "bumbu_lanjutan",
        "yes_ingredient": "gula_merah",
        "no_ingredient": None
    },
    
    # ===== KATEGORI BUMBU LANJUTAN =====
    {
        "id": "bumbu_lanjutan",
        "question": "Apakah Anda memiliki terasi di rumah?",
        "yes_next": "lada_check",
        "no_next": "lada_check",
        "yes_ingredient": "terasi",
        "no_ingredient": None
    },
    {
        "id": "lada_check",
        "question": "Apakah Anda memiliki lada hitam di rumah?",
        "yes_next": "bumbu_khusus",
        "no_next": "bumbu_khusus",
        "yes_ingredient": "lada_hitam",
        "no_ingredient": None
    },
    
    # ===== KATEGORI BUMBU KHUSUS =====
    {
        "id": "bumbu_khusus",
        "question": "Apakah Anda memiliki kluwek (bumbu rawon) di rumah?",
        "yes_next": "produk_olahan",
        "no_next": "produk_olahan",
        "yes_ingredient": "kluwek",
        "no_ingredient": None
    },
    
    # ===== KATEGORI PRODUK OLAHAN =====
    {
        "id": "produk_olahan",
        "question": "Apakah Anda memiliki keju di rumah?",
        "yes_next": "susu_check",
        "no_next": "susu_check",
        "yes_ingredient": "keju",
        "no_ingredient": None
    },
    {
        "id": "susu_check",
        "question": "Apakah Anda memiliki susu (cair atau bubuk) di rumah?",
        "yes_next": "mentega_check",
        "no_next": "mentega_check",
        "yes_ingredient": "susu",
        "no_ingredient": None
    },
    {
        "id": "mentega_check",
        "question": "Apakah Anda memiliki mentega atau margarin di rumah?",
        "yes_next": "kacang_check",
        "no_next": "kacang_check",
        "yes_ingredient": "mentega",
        "no_ingredient": None
    },
    
    # ===== KATEGORI KACANG-KACANGAN =====
    {
        "id": "kacang_check",
        "question": "Apakah Anda memiliki kacang tanah di rumah?",
        "yes_next": "minuman_check",
        "no_next": "minuman_check",
        "yes_ingredient": "kacang_tanah",
        "no_ingredient": None
    },
    
    # ===== KATEGORI MINUMAN =====
    {
        "id": "minuman_check",
        "question": "Apakah Anda memiliki teh (celup atau bubuk) di rumah?",
        "yes_next": "air_main",
        "no_next": "air_main",
        "yes_ingredient": "teh",
        "no_ingredient": None
    },
    
    # ===== KATEGORI AIR =====
    {
        "id": "air_main",
        "question": "Apakah Anda memiliki akses ke air bersih untuk memasak?",
        "yes_next": None,  # Pertanyaan terakhir
        "no_next": None,   # Pertanyaan terakhir
        "yes_ingredient": "air_bersih",
        "no_ingredient": None
    }
]

# Session storage untuk menyimpan state permainan
game_sessions = {}

class EnhancedFoodAkinator:
    def __init__(self, session_id):
        self.session_id = session_id
        self.possible_recipes = recipes_db.copy()
        self.available_ingredients = []
        self.question_history = []
        self.current_question_index = 0
        self.min_ingredients = 10  # Minimal bahan yang dibutuhkan
        self.max_questions = 40   # Maksimal pertanyaan yang diajukan
    
    def get_next_question(self):
        """Dapatkan pertanyaan berikutnya dari alur pertanyaan"""
        if len(self.question_history) >= self.max_questions:
            return None
        
        if self.current_question_index >= len(question_flow):
            return None
        
        current_q = question_flow[self.current_question_index]
        return current_q["question"]
    
    def process_answer(self, answer):
        """Proses jawaban dan update state"""
        if self.current_question_index >= len(question_flow):
            return
        
        current_q = question_flow[self.current_question_index]
        
        # Catat pertanyaan dan jawaban
        self.question_history.append({
            "question": current_q["question"],
            "answer": answer
        })
        
        # Proses jawaban
        if answer.lower() == 'yes':
            # Tambahkan ingredient jika ada
            if "yes_ingredient" in current_q and current_q["yes_ingredient"]:
                if isinstance(current_q["yes_ingredient"], list):
                    self.available_ingredients.extend(current_q["yes_ingredient"])
                else:
                    self.available_ingredients.append(current_q["yes_ingredient"])
            
            # Pindah ke pertanyaan berikutnya
            if current_q["yes_next"]:
                self._move_to_question(current_q["yes_next"])
            else:
                self.current_question_index += 1
        else:  # answer == 'no'
            # Tambahkan ingredient jika ada
            if "no_ingredient" in current_q and current_q["no_ingredient"]:
                if isinstance(current_q["no_ingredient"], list):
                    self.available_ingredients.extend(current_q["no_ingredient"])
                else:
                    self.available_ingredients.append(current_q["no_ingredient"])
            
            # Pindah ke pertanyaan berikutnya
            if current_q["no_next"]:
                self._move_to_question(current_q["no_next"])
            else:
                self.current_question_index += 1
        
        self._update_possible_recipes()
    
    def _move_to_question(self, question_id):
        """Pindah ke pertanyaan dengan ID tertentu"""
        for i, q in enumerate(question_flow):
            if q["id"] == question_id:
                self.current_question_index = i
                return
        
        # Jika tidak ditemukan, pindah ke pertanyaan berikutnya
        self.current_question_index += 1
    
    def _update_possible_recipes(self):
        """Update resep yang mungkin berdasarkan bahan yang tersedia"""
        if not self.available_ingredients:
            return
        
        updated_recipes = []
        for recipe in self.possible_recipes:
            # Hitung berapa banyak bahan yang cocok
            matching_ingredients = sum(1 for ingredient in recipe["ingredients"] 
                                     if ingredient in self.available_ingredients)
            
            # Jika ada bahan yang cocok, masukkan ke daftar
            if matching_ingredients > 0:
                updated_recipes.append(recipe)
        
        if updated_recipes:
            self.possible_recipes = updated_recipes
    
    def get_recommendations(self):
        """Dapatkan rekomendasi final, minimal 10 menu"""
        recommendations = []
        
        for recipe in self.possible_recipes:
            # Hitung berapa banyak bahan yang tersedia
            available_count = sum(1 for ingredient in recipe["ingredients"] 
                                if ingredient in self.available_ingredients)
            
            if available_count > 0:
                match_percentage = (available_count / len(recipe["ingredients"])) * 100
                missing_ingredients = [ing for ing in recipe["ingredients"] 
                                     if ing not in self.available_ingredients]
                
                recommendations.append({
                    "name": recipe["name"],
                    "description": recipe["description"],
                    "match_percentage": match_percentage,
                    "missing_ingredients": missing_ingredients,
                    "available_count": available_count
                })
        
        # Urutkan berdasarkan persentase kecocokan dan jumlah bahan yang tersedia
        recommendations.sort(key=lambda x: (x["match_percentage"], x["available_count"]), reverse=True)
        
        # Pastikan minimal 10 rekomendasi
        if len(recommendations) < 10:
            # Tambahkan resep lain yang mungkin bisa dibuat dengan sedikit tambahan bahan
            for recipe in recipes_db:
                if not any(r["name"] == recipe["name"] for r in recommendations):
                    available_count = sum(1 for ingredient in recipe["ingredients"] 
                                        if ingredient in self.available_ingredients)
                    if available_count > 0:  # Minimal 1 bahan yang cocok
                        match_percentage = (available_count / len(recipe["ingredients"])) * 100
                        missing_ingredients = [ing for ing in recipe["ingredients"] 
                                             if ing not in self.available_ingredients]
                        
                        recommendations.append({
                            "name": recipe["name"],
                            "description": recipe["description"],
                            "match_percentage": match_percentage,
                            "missing_ingredients": missing_ingredients,
                            "available_count": available_count
                        })
                        
                        # Jika sudah mencapai 10 rekomendasi, berhenti
                        if len(recommendations) >= 10:
                            break
        
        # Urutkan ulang dan ambil minimal 10 rekomendasi
        recommendations.sort(key=lambda x: (x["match_percentage"], x["available_count"]), reverse=True)
        return recommendations[:max(10, len(recommendations))]  # Minimal 10 rekomendasi

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    session_id = str(random.randint(100000, 999999))
    akinator = EnhancedFoodAkinator(session_id)
    game_sessions[session_id] = akinator
    
    question = akinator.get_next_question()
    
    return jsonify({
        "session_id": session_id,
        "question": question,
        "question_count": len(akinator.question_history),
        "max_questions": akinator.max_questions,
        "ingredients_count": len(akinator.available_ingredients),
        "min_ingredients": akinator.min_ingredients
    })

@app.route('/answer', methods=['POST'])
def answer():
    data = request.get_json()
    session_id = data.get('session_id')
    answer = data.get('answer')
    
    if session_id not in game_sessions:
        return jsonify({"error": "Session not found"}), 400
    
    akinator = game_sessions[session_id]
    akinator.process_answer(answer)
    
    # Dapatkan pertanyaan berikutnya
    next_question = akinator.get_next_question()
    
    if next_question and len(akinator.available_ingredients) < akinator.min_ingredients:
        return jsonify({
            "question": next_question,
            "question_count": len(akinator.question_history),
            "max_questions": akinator.max_questions,
            "ingredients_count": len(akinator.available_ingredients),
            "min_ingredients": akinator.min_ingredients,
            "available_ingredients": akinator.available_ingredients,
            "finished": False
        })
    else:
        # Game selesai, berikan rekomendasi
        recommendations = akinator.get_recommendations()
        return jsonify({
            "finished": True,
            "recommendations": recommendations,
            "available_ingredients": akinator.available_ingredients,
            "question_count": len(akinator.question_history),
            "total_ingredients": len(akinator.available_ingredients)
        })

@app.route('/restart', methods=['POST'])
def restart():
    data = request.get_json()
    session_id = data.get('session_id')
    
    if session_id in game_sessions:
        del game_sessions[session_id]
    
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)
