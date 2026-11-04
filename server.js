const { default: makeWASocket, useMultiFileAuthState } = require('@whiskeysockets/baileys');
const express = require('express');
const app = express();
app.use(express.json());

let sock;

async function connectToWhatsApp() {
    const { state, saveCreds } = await useMultiFileAuthState('auth_info_baileys');
    sock = makeWASocket({
        auth: state,
        printQRInTerminal: true
    });

    sock.ev.on('creds.update', saveCreds);
    sock.ev.on('connection.update', (update) => {
        const { connection } = update;
        if (connection === 'open') {
            console.log('Bot WhatsApp Berjaya Terhubung!');
        }
    });
}

// Endpoint untuk menerima pesanan daripada skrip Python
app.post('/send-message', async (req, res) => {
    const { number, message } = req.body;
    try {
        const jid = `${number}@s.whatsapp.net`;
        await sock.sendMessage(jid, { text: message });
        res.status(200).json({ status: 'Success' });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

connectToWhatsApp();
app.listen(3000, () => console.log('WhatsApp Webhook Server berjalan pada port 3000'));