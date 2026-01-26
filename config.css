:root { 
    --admin-red: #ef4444; 
    --accent: #38bdf8; 
    --glass: rgba(255, 255, 255, 0.03);
}

body { 
    background: #000; 
    color: white; 
    font-family: 'Fredoka', sans-serif; 
    overflow: hidden; 
    margin: 0; 
}

/* Neural Background Pulse */
@keyframes neuralDrift {
    0% { background-position: 0% 50%; opacity: 0.8; }
    50% { background-position: 100% 50%; opacity: 1; }
    100% { background-position: 0% 50%; opacity: 0.8; }
}

#desktop-view {
    background: radial-gradient(circle at center, #020617 0%, #000 100%);
    background-size: 200% 200%;
    animation: neuralDrift 10s ease infinite;
}

.glass { 
    background: var(--glass); 
    backdrop-filter: blur(40px); 
    border: 1px solid rgba(255, 255, 255, 0.1); 
}

/* Settings Slide-out */
.settings-menu {
    position: fixed;
    right: -450px;
    top: 20px;
    bottom: 20px;
    width: 380px;
    z-index: 1000;
    transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}

.settings-menu.open { right: 20px; }

/* Custom Scrollbar for Chat & Settings */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }

.msg-container { display: flex; align-items: flex-end; gap: 12px; margin-bottom: 20px; width: 100%; animation: slideUp 0.3s ease; }
.msg-user { flex-direction: row-reverse; }
.bubble { max-width: 70%; padding: 14px 20px; font-size: 14px; border-radius: 24px; }
.bubble-bot { background: rgba(255,255,255,0.05); border-bottom-left-radius: 4px; }
.bubble-user { background: var(--accent); color: #000; font-weight: 600; border-bottom-right-radius: 4px; }

.admin-glow { border: 1px solid var(--admin-red) !important; box-shadow: 0 0 15px rgba(239, 68, 68, 0.2); }
.admin-text { color: var(--admin-red) !important; }

@keyframes slideUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
