import subprocess
import json
import requests

# 1. Jalankan perintah CLI kart untuk mendapatkan status/maklumat terkini
def get_kart_status():
    try:
        # Menjalankan perintah CLI kart status
        result = subprocess.run(["kart", "status"], capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        return data
    except Exception as e:
        print(f"Ralat semasa menjalankan kart CLI: {e}")
        return None

# 2. Formatkan maklumat JSON menjadi laporan perenggan WhatsApp
def generate_whatsapp_report(kart_data):
    if not kart_data:
        return "⚠️ *Laporan Gagal*: Tidak dapat mengambil data daripada kart CLI."

    # Contoh ekstraksi data daripada JSON kart
    match_info = kart_data.get("lastMatch", {})
    rating = kart_data.get("rating", "N/A")
    rank = kart_data.get("rank", "N/A")
    replay_url = match_info.get("replayUrl", "-")
    opponent = match_info.get("opponent", "Lawan")
    result_status = "MENANG 🎉" if match_info.get("won") else "KALAH 😞"

    # Menyusun teks laporan mengikut format pesanan WhatsApp
    report = f"""
*Laporan Ronde Ladder Perlawanan*

*Hasil*: {result_status} vs *{opponent}*

• *Replay*: {replay_url}
• *Rating*: {rating}
• *Rank*: #{rank}

_Skrip berjalan secara automatik menerusi sistem kart CLI._
"""
    return report

# 3. Hantar pesanan ke WhatsApp Webhook / API
def send_to_whatsapp(message):
    url = "http://localhost:3000/send-message"  # URL perkhidmatan bot WhatsApp anda
    payload = {
        "number": "628xxxxxxxxxx",  # Nombor WhatsApp anda (serta kod negara)
        "message": message
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        print("Laporan berjaya dihantar ke WhatsApp:", response.status_code)
    except Exception as e:
        print("Ralat penghantaran WhatsApp:", e)

if __name__ == "__main__":
    data = get_kart_status()
    report_text = generate_whatsapp_report(data)
    send_to_whatsapp(report_text)