import random
import cv2
import numpy as np
import pyautogui
import pytesseract
import time
import pygame
import os
import sys
import keyboard
import threading
import tkinter as tk
from tkinter import messagebox, ttk
import winsound
from PIL import Image, ImageGrab
import pygetwindow as gw
from difflib import SequenceMatcher
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import json
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except:
        pass

if getattr(sys, 'frozen', False):
    BASE_PATH = os.path.dirname(sys.executable)
else:
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# Redirection des erreurs vers un fichier log
try:
    _log_dir = os.path.join(BASE_PATH, "log")
    os.makedirs(_log_dir, exist_ok=True)
    _err_file = open(os.path.join(_log_dir, "error_log.txt"), "a", encoding="utf-8")
    sys.stderr = _err_file
except: pass

DOSS_MUSIQUE = os.path.join(BASE_PATH, "music")
ICONE_PATH = os.path.join(BASE_PATH, "dofus-music.ico")
DOSS_LOG = os.path.join(BASE_PATH, "log")
FILE_CONFIG = os.path.join(DOSS_LOG, "config_app.json")
FILE_LOG = os.path.join(DOSS_LOG, "detection_log.json")

def trouver_tesseract():
    chemins = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
        os.path.join(os.environ.get('LOCALAPPDATA', ''), r'Tesseract-OCR\tesseract.exe')
    ]
    for p in chemins:
        if os.path.exists(p):
            return p
    import shutil
    path_système = shutil.which("tesseract")
    if path_système:
        return path_système
    return None

TESS_PATH = trouver_tesseract()

if not TESS_PATH:
    root_err = tk.Tk(); root_err.withdraw()
    messagebox.showerror("Tesseract Manquant", 
        "Tesseract OCR n'est pas détecté sur votre système.\n\n"
        "1. Installez Tesseract (version 64-bit de préférence).\n"
        "2. Si déjà installé, vérifiez le dossier : C:\\Program Files\\Tesseract-OCR")
    root_err.destroy(); sys.exit()

pytesseract.pytesseract.tesseract_cmd = TESS_PATH

BG_MAIN = "#312C2A"      
BG_HEADER = "#383838"    
BG_SHADOW = "#1a1a1a"    
BORDER_COLOR = "#25211f" 
FG_LIGHT = "#e0e0e0"     
BG_WIDGET = "#574E45"    
ACCENT_GREEN = "#4caf50" 
ACCENT_BLUE = "#64b5f6"
ACCENT_RED = "#ef5350"
ACCENT_GREEN_CLAIR = "#D1FF66"

ZONES_FRIGOST = ["frigost", "creperg", "bourgade", "casjourfin", "forpet", "jardhiv",
                 "larmeberceau", "portdegivre", "rempvent", "ruchglours"]
ZONES_PANDALA = ["aerdala", "plantala", "feudala", "terrdala", "akwadala", "grobe"]
ZONES_OTOMAI  = ["hakam", "otomai", "vzoth", "vcanop"]

NOMS_PROPRES = {
    "menu": "Démarrage", "abra": "Forêt des Abraknydes", "gelée": "Péninsule des Gelées", "bwork": "Campement des Bworks", 
    "chamakna": "Chateau d'Amakna", "ankmarecage": "Marécage d'Amakna", "marecage": "Marécage", "drag": "Presqu'île des Dragoeufs", 
    "plageamakna": "Plage d'Amakna", "karton": "Île de Kartonpath", "mcraque": "Montagne des Craqueleurs", 
    "mbcraque": "Montagne basse des Craqueleurs", "amakna": "Amakna", "cimetière": "Cimetière", "taverne": "Taverne", 
    "pastrub": "Prairie d'Astrub", "astrub": "Astrub", "fastrubkoala": "Forêt d'Astrub", 
    "incarnam": "Incarnam", "bonta": "Bonta", "brakmar": "Brâkmar", "trool": "Foire du Trool", "mino": "Île du Minotoror", 
    "moon": "Île de Moon", "wabbit": "Île des Wabbits", "sidimote": "Landes de Sidimote", "sufokia": "Sufokia", 
    "portdegivre": "Port de Givre", "bourgade": "La Bourgade & Les Champs de glace", "frigost": "Frigost", 
    "larmeberceau": "Larmes d'Ouronigride & Berceau d'Alma", "creperg": "Crevasse Perge", "forpet": "Forêt Pétrifiée", 
    "martegel": "Royaume des Martegel", "ruchglours": "Mont Torrideau & Ruche des Gloursons", "rempvent": "Remparts à Vent", 
    "jardhiv": "Jardins d'Hiver", "tourclep": "Tour de la Clepsydre", "casjourfin": "Caserne du Jour sans fin", 
    "cania": "Plaines de Cania", "vpandala": "Village de Pandala", "pandala": "Île de Pandala", "vcanop": "Village de la Canopée", 
    "cavemine": "Mines & Souterrains", "vzoth": "Villages des Zoths & Brigandins", "tourboto": "Tourbière", 
    "otomai": "Île d'Otomaï", "hakam": "Feuillage de l'Arbre Hakam", "dimobs": "Dimension Obscure", 
    "ecaflipus": "Dimension Ecaflipus", "enutrosor": "Dimension Enutrosor", "srambad": "Dimension Srambad", 
    "xelorium": "Dimension Xélorium", "vkoalak": "Village des Éleveurs", "koalak": "Montagne des Koalaks", 
    "mkoalak": "Vallée de la Morh'kitu", "forpinperdu": "Fôret des Pins perdus", "porcos": "Territoire de Porcos & Dragon cochon",
    "havresac": "Havre-Sac", "vulkania": "Île de Vulkania", "nowel": "Île de Nowel & Nowel en Amakna",
    "grobe": "Île de Grobe", "aerdala": "Aerdala", "plantala": "Fôret de Pandala & Plantala", "feudala": "Feudala", "terrdala": "Terrdala", "akwadala": "Akwadala",
    "oreeenchant": "Orée Enchantée", "dedaledv": "Dédale du Dark Vlad", "bibli": "Bibliotemple de l'Almanax", "donjon": "Ambiance Donjon",
    "osavora": "Osatopia Temporis VII","ingloriom": "Inglorium Wakfu la série OST",
    "tfeca": "Temple Féca", "tosamodas": "Temple Osamodas", "tenutrof": "Temple Enutrof", 
    "tsram": "Temple Sram", "txelor": "Temple Xélor", "tecaflip": "Temple Écaflip", "teniripsa": "Temple Eniripsa", 
    "tiop": "Temple Iop", "tcra": "Temple Crâ", "tsadida": "Temple Sadida", "tsacrieur": "Temple Sacrieur", 
    "tpandawa": "Temple Pandawa", "troublard": "Temple Roublard", "tzobal": "Temple Zobal", "tsteamer": "Temple Steamer",
    "teliotrop": "Temple Eliotrope", "touginak": "Temple Ouginak", "thuppermage": "Temple Huppermage"
}

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None

    def show_tip(self):
        if self.tip_window or not self.text: return
        x, y, _, _ = self.widget.bbox("insert")
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tw.wm_attributes("-topmost", True)
        tk.Label(tw, text=self.text, justify=tk.LEFT, background="#ffffe1", 
                 relief=tk.SOLID, borderwidth=1, font=("Arial", 8)).pack()

    def hide_tip(self):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

def create_tooltip(widget, text):
    tool_tip = ToolTip(widget, text)
    widget.bind('<Enter>', lambda e: tool_tip.show_tip())
    widget.bind('<Leave>', lambda e: tool_tip.hide_tip())

class ZoneSelector(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app.root)
        self.app = app
        self.overrideredirect(True)
        self.attributes('-alpha', 0.3, '-topmost', True)
        self.configure(bg="pink")
        self.geometry(self.app.zone_ocr_rect)
        self.label = tk.Label(self, text="ZONE DE RECHERCHE\n(Clic Droit pour redimensionner)", 
                              fg="black", bg="pink", font=("Arial", 8, "bold"))
        self.label.pack(expand=True)
        self.bind("<Button-1>", self.start_move)
        self.bind("<B1-Motion>", self.do_move)
        self.bind("<Button-3>", self.start_resize)
        self.bind("<B3-Motion>", self.do_resize)

    def start_move(self, event): 
        self.x, self.y = event.x, event.y

    def do_move(self, event):
        dx, dy = event.x - self.x, event.y - self.y
        new_x = self.winfo_x() + dx
        new_y = self.winfo_y() + dy
        self.geometry(f"+{new_x}+{new_y}")
        self.app.zone_ocr_rect = self.get_rect()

    def start_resize(self, event): 
        self.x, self.y = event.x, event.y

    def do_resize(self, event):
        nw = max(50, self.winfo_width() + (event.x - self.x))
        nh = max(20, self.winfo_height() + (event.y - self.y))
        self.geometry(f"{nw}x{nh}")
        self.x, self.y = event.x, event.y
        self.app.zone_ocr_rect = self.get_rect()

    def get_rect(self):
        return f"{self.winfo_width()}x{self.winfo_height()}+{self.winfo_x()}+{self.winfo_y()}"

class DofusMusicApp:
    def __init__(self, root):
        self.dernier_etat_combat = False
        self.derniere_zone_detectee = ""
        self.en_combat = False
        self.root = root
        self.root.title("DM")
        self.root.overrideredirect(True) 
        self.appliquer_icone(self.root)
        
        self.root.geometry("200x150") 
        self.root.configure(bg=BG_MAIN, highlightbackground=BORDER_COLOR, highlightthickness=1)
        self.root.attributes('-alpha', 0.9, '-topmost', True)

        self.header_bar = tk.Frame(self.root, bg=BG_HEADER, height=20)
        self.header_bar.pack(side="top", fill="x")
        self.header_bar.pack_propagate(False)
        
        try:
            if os.path.exists(ICONE_PATH):
                from PIL import Image, ImageTk
                img = Image.open(ICONE_PATH).resize((16, 16), Image.Resampling.LANCZOS)
                self.ico_img = ImageTk.PhotoImage(img)
                self.lbl_ico = tk.Label(self.header_bar, image=self.ico_img, bg=BG_HEADER)
                self.lbl_ico.pack(side="left", padx=(5, 2))
        except: pass

        tk.Label(self.header_bar, text="Dofus Music Reload", font=("Arial", 8, "bold"), 
                 bg=BG_HEADER, fg=ACCENT_GREEN_CLAIR).pack(side="left")

        self.btn_help = tk.Button(self.header_bar, text="?", command=self.afficher_readme,
                                  font=("Arial", 7, "bold"), bg=BG_HEADER, fg=FG_LIGHT,
                                  bd=0, cursor="hand2", activebackground=BG_WIDGET)
        self.btn_help.pack(side="right", padx=5)
        
        tk.Frame(self.root, bg=BG_SHADOW, height=1).pack(side="top", fill="x")

        self.main_container = tk.Frame(self.root, bg=BG_MAIN)
        self.main_container.pack(fill="both", expand=True)

        self.zone_ocr_rect = "573x30+5+61"
        self.selector = None

        self.root.bind("<Button-1>", self.demarrer_deplacement)
        self.root.bind("<B1-Motion>", self.deplacer_fenetre)
        
        self.actif = True
        self.musique_actuelle = ""
        self.win_config = None
        self.win_help = None
        
        self.version_choisie = tk.StringVar(value="1")
        self.prefs_perso = {z: "1" for z in NOMS_PROPRES.keys()}
        self.volume_sauvegarde = 15
        self.charger_configuration()
        pygame.mixer.init()
        pygame.mixer.music.set_volume(self.volume_sauvegarde / 100)

        if not os.path.exists(DOSS_MUSIQUE) or not any(
            f.endswith(".wav") for _, _, files in os.walk(DOSS_MUSIQUE) for f in files
        ):
            msg = "Aucun fichier .wav trouvé dans le dossier 'music'.\nVérifiez que le dossier existe et contient des fichiers audio."
            self.root.after(500, lambda: messagebox.showwarning("Dossier musique", msg))

        if not os.path.exists(FILE_CONFIG):
            self.initialiser_prefs_auto()
            self.root.after(1000, self.afficher_readme)

        for zone_id in list(self.prefs_perso.keys()):
            if not zone_id.endswith("_c"):
                key_c = zone_id + "_c"
                if key_c not in self.prefs_perso:
                    self.prefs_perso[key_c] = self.prefs_perso[zone_id]

        self.frame_info = tk.Frame(self.main_container, bg=BG_MAIN)
        self.frame_info.place(x=5, y=5, width=145, height=90)
        
        tk.Label(self.frame_info, text="Choix de la version :", font=("Arial", 7, "bold"), bg=BG_MAIN, fg=FG_LIGHT).pack()
        f_radio = tk.Frame(self.frame_info, bg=BG_MAIN)
        f_radio.pack()
        rb_opt = {"bg": BG_MAIN, "fg": FG_LIGHT, "selectcolor": "#1a1817", "activebackground": BG_MAIN, "font": ("Arial", 7), "command": self.actualiser_version}
        tk.Radiobutton(f_radio, text="1.29", variable=self.version_choisie, value="1", **rb_opt).pack(side=tk.LEFT)
        tk.Radiobutton(f_radio, text="2.0", variable=self.version_choisie, value="2", **rb_opt).pack(side=tk.LEFT)
        tk.Radiobutton(f_radio, text="Perso", variable=self.version_choisie, value="3", **rb_opt).pack(side=tk.LEFT)
        
        self.label_status = tk.Label(self.frame_info, text="STATUT : ACTIF", fg=ACCENT_GREEN, bg=BG_MAIN, font=("Arial", 7, "bold"))
        self.label_status.pack(pady=2)
        self.label_music = tk.Label(self.frame_info, text="Accueil", fg=ACCENT_GREEN_CLAIR, bg=BG_MAIN, font=("Arial", 7), wraplength=130)
        self.label_music.pack()

        self.frame_vol = tk.Frame(self.main_container, bg=BG_MAIN)
        self.frame_vol.place(x=155, y=5, width=35, height=90)
        self.slider_vol = tk.Scale(self.frame_vol, from_=100, to=0, orient=tk.VERTICAL, command=self.ajuster_volume, length=75, width=8, sliderlength=12, bg=BG_MAIN, fg=FG_LIGHT, font=("Arial", 6), highlightthickness=0, troughcolor="#1a1817")
        self.slider_vol.set(self.volume_sauvegarde)
        self.slider_vol.pack()

        btn_base_style = {"bg": BG_WIDGET, "relief": tk.RAISED, "borderwidth": 2, "activebackground": "#6d6257", "activeforeground": "white"}
        
        self.btn_zone = tk.Button(self.main_container, text="🔍", command=self.toggle_selector, font=("Arial", 19), fg=ACCENT_GREEN_CLAIR, **btn_base_style)
        self.btn_zone.place(x=37, y=95, width=28, height=28)
        
        self.btn_config = tk.Button(self.main_container, text="⚙", command=self.ouvrir_config, font=("Arial", 15), fg=FG_LIGHT, **btn_base_style)
        self.btn_config.place(x=70, y=95, width=28, height=28)
        
        self.btn_toggle = tk.Button(self.main_container, text="⏻", command=self.toggle, font=("Arial", 15, "bold"), fg=FG_LIGHT, **btn_base_style)
        self.btn_toggle.place(x=103, y=95, width=28, height=28)
        
        self.btn_quit = tk.Button(self.main_container, text="✕", command=self.quitter, font=("Arial", 15, "bold"), fg=ACCENT_RED, **btn_base_style)
        self.btn_quit.place(x=136, y=95, width=28, height=28)

        self.header_bar.bind("<Button-1>", self.demarrer_deplacement)
        self.header_bar.bind("<B1-Motion>", self.deplacer_fenetre)

        create_tooltip(self.btn_zone, "Définir la zone de recherche (Nom de zone)")
        create_tooltip(self.btn_config, "Réglages des versions (1.29 / 2.0) par zone")
        create_tooltip(self.btn_toggle, "Activer/Désactiver (F7)")
        create_tooltip(self.btn_quit, "Quitter l'application")
        create_tooltip(self.slider_vol, "Volume de la musique")
        keyboard.add_hotkey('f7', self.toggle)
        keyboard.add_hotkey('ctrl+²', self.toggle_ocr_debug)
        self.win_ocr_debug = None
        self.win_combat_highlight = None
        self._log_lock = threading.Lock()
        self.log_data = self.charger_log()
        self._cpu_samples = []
        self._cpu_lock = threading.Lock()
        try:
            import psutil
            self._process = psutil.Process(os.getpid())
            self._process.cpu_percent(interval=None)  # Premier appel d'initialisation
            self._cpu_count = psutil.cpu_count(logical=True) or 1
        except:
            self._process = None
            self._cpu_count = 1
        self.root.after(200, lambda: self.ajuster_volume(self.volume_sauvegarde))
        self.root.bind("<FocusIn>", lambda e: self.root.attributes('-topmost', True))
        threading.Thread(target=self.boucle_focus, daemon=True).start()
        self.root.after(2000, self._tick_focus)
        self.jouer_fichier(os.path.join(DOSS_MUSIQUE, "menu.wav"), "Accueil")
        threading.Thread(target=self.boucle_scan, daemon=True).start()

    def toggle_ocr_debug(self):
        if self.win_ocr_debug is not None and self.win_ocr_debug.winfo_exists():
            self.win_ocr_debug.destroy()
            self.win_ocr_debug = None
            self.masquer_highlight()
            return

        self.win_ocr_debug = tk.Toplevel(self.root)
        self.win_ocr_debug.overrideredirect(True)
        self.win_ocr_debug.configure(bg="#0a0a0a", highlightbackground=BORDER_COLOR, highlightthickness=1)
        self.win_ocr_debug.attributes('-alpha', 0.92, '-topmost', True)

        self.root.update_idletasks()
        rx = self.root.winfo_rootx()
        ry = self.root.winfo_rooty()
        rh = self.root.winfo_height()
        rw = self.root.winfo_width()
        self.win_ocr_debug.geometry(f"{rw}x95+{rx}+{ry + rh + 4}")

        tk.Label(self.win_ocr_debug, text="OCR DEBUG", font=("Consolas", 7, "bold"),
                 bg="#0a0a0a", fg="#555").pack(anchor="w", padx=6, pady=(3,0))
        self.lbl_ocr_debug = tk.Label(self.win_ocr_debug, text="En attente...",
                 font=("Consolas", 8), bg="#0a0a0a", fg="#00ff99", wraplength=190, justify="left")
        self.lbl_ocr_debug.pack(anchor="w", padx=6)
        self.lbl_ocr_zone = tk.Label(self.win_ocr_debug, text="Zone : -- | Combat : --",
                 font=("Consolas", 7), bg="#0a0a0a", fg="#aaa", wraplength=190, justify="left")
        self.lbl_ocr_zone.pack(anchor="w", padx=6)
        self.lbl_ocr_fiabilite = tk.Label(self.win_ocr_debug, text="Fiabilité zone : --%",
                 font=("Consolas", 7), bg="#0a0a0a", fg="#aaa", wraplength=190, justify="left")
        self.lbl_ocr_fiabilite.pack(anchor="w", padx=6)
        self.lbl_ocr_time = tk.Label(self.win_ocr_debug, text="Dernier scan : --:--:--",
                 font=("Consolas", 7), bg="#0a0a0a", fg="#444", wraplength=190, justify="left")
        self.lbl_ocr_time.pack(anchor="w", padx=6, pady=(0, 3))

    def afficher_highlight(self, x, y, w, h):
        try:
            if self.win_combat_highlight is None or not self.win_combat_highlight.winfo_exists():
                self.win_combat_highlight = tk.Toplevel(self.root)
                self.win_combat_highlight.overrideredirect(True)
                self.win_combat_highlight.attributes('-alpha', 0.5, '-topmost', True)
                self.win_combat_highlight.configure(
                    bg=ACCENT_RED,
                    highlightbackground=ACCENT_RED,
                    highlightthickness=3
                )
                tk.Frame(self.win_combat_highlight, bg=ACCENT_RED).pack(expand=True, fill="both")
            self.win_combat_highlight.geometry(f"{w}x{h}+{x}+{y}")
            self.win_combat_highlight.attributes('-topmost', True)
        except: pass

    def masquer_highlight(self):
        try:
            if self.win_combat_highlight is not None and self.win_combat_highlight.winfo_exists():
                self.win_combat_highlight.destroy()
                self.win_combat_highlight = None
        except: pass

    def charger_log(self):
        if os.path.exists(FILE_LOG):
            try:
                with open(FILE_LOG, "r", encoding="utf-8") as f:
                    return json.load(f)
            except: pass
        return {}

    def enregistrer_detection(self, zone_id, succes=True, txt_ocr=""):
        if not zone_id:
            return
        with self._log_lock:
            if zone_id not in self.log_data:
                self.log_data[zone_id] = {
                    "nom": NOMS_PROPRES.get(zone_id, zone_id),
                    "historique": [],
                    "erreurs_ocr": [],
                    "derniere_visite": ""
                }
            entry = self.log_data[zone_id]
            if "erreurs_ocr" not in entry:
                entry["erreurs_ocr"] = []
            entry["historique"].append(1 if succes else 0)
            if len(entry["historique"]) > 500:
                entry["historique"].pop(0)
            if succes:
                entry["derniere_visite"] = time.strftime("%d/%m/%Y %H:%M:%S")
            elif txt_ocr:
                txt_strip = txt_ocr.strip()
                trouve = False
                for i, err in enumerate(entry["erreurs_ocr"]):
                    err_txt = err["txt"] if isinstance(err, dict) else err
                    if err_txt == txt_strip:
                        count = err["count"] if isinstance(err, dict) else 1
                        entry["erreurs_ocr"][i] = {"txt": txt_strip, "count": count + 1}
                        trouve = True
                        break
                if not trouve:
                    entry["erreurs_ocr"].append({"txt": txt_strip, "count": 1})
                    if len(entry["erreurs_ocr"]) > 10:
                        entry["erreurs_ocr"].pop(0)

    def sauvegarder_log(self):
        try:
            with self._log_lock:
                data_copy = json.loads(json.dumps(self.log_data))
            with open(FILE_LOG, "w", encoding="utf-8") as f:
                json.dump(data_copy, f, ensure_ascii=False, indent=2)
            self.exporter_log_txt(data_copy)
        except: pass

    def exporter_log_txt(self, data=None):
        try:
            if data is None:
                with self._log_lock:
                    data = json.loads(json.dumps(self.log_data))
            path_txt = os.path.join(DOSS_LOG, "detection_log.txt")
            lignes = []
            lignes.append("=" * 55)
            lignes.append("  DOFUS MUSIC RELOAD — LOG DE DÉTECTION")
            lignes.append(f"  Mis à jour : {time.strftime('%d/%m/%Y %H:%M:%S')}")
            lignes.append("=" * 55)
            lignes.append("")
            # Stats CPU
            with self._cpu_lock:
                cpu_samples = list(self._cpu_samples)
            if cpu_samples:
                lignes.append("┌─ STATS CPU (processus)")
                lignes.append(f"│  Pic max   : {max(cpu_samples):.1f}%")
                lignes.append(f"│  Pic min   : {min(cpu_samples):.1f}%")
                lignes.append(f"│  Moyenne   : {sum(cpu_samples)/len(cpu_samples):.1f}%")
                lignes.append(f"│  Échantillons : {len(cpu_samples)}/500")
                lignes.append("└─────────────────────────────────────────────")
                lignes.append("")
            zones_triees = sorted(data.items(),
                key=lambda x: x[1].get("derniere_visite", ""), reverse=True)
            for zone_id, data in zones_triees:
                historique = data.get("historique", [])
                total = len(historique)
                coherents = sum(historique)
                pct = (coherents / total * 100) if total > 0 else 0
                lignes.append(f"┌─ {data.get('nom', zone_id)}")
                lignes.append(f"│  Scans analysés  : {total}/500")
                lignes.append(f"│  Fiabilité       : {pct:.1f}%")
                erreurs = data.get("erreurs_ocr", [])
                if erreurs:
                    lignes.append(f"│  Dernières erreurs OCR :")
                    for err in reversed(erreurs):
                        if isinstance(err, dict):
                            count = err.get("count", 1)
                            txt = err.get("txt", "")
                            suffix = f" x{count}" if count > 1 else ""
                            lignes.append("│    • \"" + txt + "\"" + suffix)
                        else:
                            lignes.append("│    • \"" + err + "\"")
                lignes.append(f"└  Dernière visite : {data.get('derniere_visite', '--')}")
                lignes.append("")
            with open(path_txt, "w", encoding="utf-8") as f:
                f.write("\n".join(lignes))
        except: pass

    def nettoyer_erreurs_transition(self, ancienne_zone, nouvelle_zone, base_detections):
        if not ancienne_zone or not nouvelle_zone or ancienne_zone == nouvelle_zone:
            return
        with self._log_lock:
            if ancienne_zone not in self.log_data:
                return
            entry = self.log_data[ancienne_zone]
            erreurs = entry.get("erreurs_ocr", [])
            historique = entry.get("historique", [])
            if not erreurs:
                return
            mots_nouvelle_zone = [mot for mot, fich, _ in base_detections if fich == nouvelle_zone]
            erreurs_a_garder = []
            nb_retirees = 0
            for err in erreurs:
                err_lower = (err["txt"] if isinstance(err, dict) else err).lower()
                est_transition = False
                for mot in mots_nouvelle_zone:
                    if "temple" in mot:
                        condition = mot in err_lower
                    else:
                        condition = mot in err_lower or SequenceMatcher(None, err_lower, mot).ratio() > 0.8
                    if condition:
                        est_transition = True
                        break
                if est_transition:
                    nb_retirees += 1
                else:
                    erreurs_a_garder.append(err)
            if nb_retirees > 0:
                entry["erreurs_ocr"] = erreurs_a_garder
                retirees = 0
                nouvel_historique = list(historique)
                for i in range(len(nouvel_historique) - 1, -1, -1):
                    if retirees >= nb_retirees:
                        break
                    if nouvel_historique[i] == 0:
                        nouvel_historique.pop(i)
                        retirees += 1
                entry["historique"] = nouvel_historique

    def _tick_focus(self):
        """Appelé toutes les 2s depuis le thread principal via root.after."""
        try:
            if self.root.winfo_exists():
                self.root.attributes('-topmost', True)
            if self.win_ocr_debug is not None and self.win_ocr_debug.winfo_exists():
                self.win_ocr_debug.attributes('-topmost', True)
            if self.actif and self.musique_actuelle and self.musique_actuelle not in ("mute", ""):
                try:
                    if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.load(self.musique_actuelle)
                        pygame.mixer.music.play(loops=-1, fade_ms=250)
                except: pass
        except: pass
        self.root.after(2000, self._tick_focus)

    def boucle_focus(self):
        dernier_log = time.time()
        while True:
            try:
                # Échantillon CPU toutes les 2s
                try:
                    if self._process is not None:
                        cpu = self._process.cpu_percent(interval=None) / self._cpu_count
                        if cpu > 0:  # Ignorer les 0 parasites du premier appel
                            with self._cpu_lock:
                                self._cpu_samples.append(cpu)
                                if len(self._cpu_samples) > 500:
                                    self._cpu_samples.pop(0)
                except: pass
                intervalle_log = 10 if (self.win_ocr_debug is not None and self.win_ocr_debug.winfo_exists()) else 300
                if time.time() - dernier_log >= intervalle_log:
                    self.sauvegarder_log()
                    dernier_log = time.time()
            except: break
            time.sleep(2)

    def detecter_combat(self, screenshot=None):
        try:
            from PIL import ImageGrab
            if screenshot is None:
                screenshot = ImageGrab.grab(all_screens=True)
            screen = np.array(screenshot)
            screen_gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
            dossier_ui = os.path.join(BASE_PATH, "ui")
            if not os.path.exists(dossier_ui):
                ref_paths = [os.path.join(BASE_PATH, "ui_combat.png")]
            else:
                ref_paths = [os.path.join(dossier_ui, f) for f in os.listdir(dossier_ui) 
                             if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if not ref_paths:
                return False
            for path in ref_paths:
                template = cv2.imread(path, 0)
                if template is None: continue
                res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(res)
                if max_val > 0.8:
                    if self.win_ocr_debug is not None and self.win_ocr_debug.winfo_exists():
                        th, tw = template.shape[:2]
                        try:
                            from PIL import ImageGrab as _IG
                            bbox = _IG.grab(all_screens=True).getbbox()
                            offset_x = screenshot.getbbox()[0] if hasattr(screenshot, 'getbbox') else 0
                        except:
                            offset_x = 0
                        import ctypes
                        try:
                            sm_xvscreen = ctypes.windll.user32.GetSystemMetrics(76)
                            sm_yvscreen = ctypes.windll.user32.GetSystemMetrics(77)
                        except:
                            sm_xvscreen, sm_yvscreen = 0, 0
                        rx = max_loc[0] + sm_xvscreen
                        ry = max_loc[1] + sm_yvscreen
                        self.root.after(0, lambda x=rx, y=ry, w=tw, h=th:
                            self.afficher_highlight(x, y, w, h))
                    return True
            if self.win_ocr_debug is not None and self.win_ocr_debug.winfo_exists():
                self.root.after(0, self.masquer_highlight)
            return False
        except Exception as e:
            print(f"Erreur détection : {e}")
            return False

    def toggle_selector(self):
        if self.selector and self.selector.winfo_exists():
            self.selector.destroy()
            self.btn_zone.config(bg=BG_WIDGET)
            self.sauvegarder_configuration()
        else:
            self.selector = ZoneSelector(self)
            self.btn_zone.config(bg=ACCENT_BLUE)

    def appliquer_icone(self, fenetre):
        try:
            if os.path.exists(ICONE_PATH): fenetre.iconbitmap(ICONE_PATH)
        except: pass

    def initialiser_prefs_auto(self):
        dossier_3 = os.path.join(DOSS_MUSIQUE, "3")
        random_dispo = os.path.exists(dossier_3) and any(f.endswith(".wav") for f in os.listdir(dossier_3))

        for zone_id in NOMS_PROPRES.keys():
            if zone_id == "menu":
                continue
            nom_expl = "pandala" if zone_id in ZONES_PANDALA else zone_id
            if os.path.exists(os.path.join(DOSS_MUSIQUE, "1", f"1{nom_expl}.wav")):
                self.prefs_perso[zone_id] = "1"
            elif os.path.exists(os.path.join(DOSS_MUSIQUE, "2", f"2{nom_expl}.wav")):
                self.prefs_perso[zone_id] = "2"
            else:
                self.prefs_perso[zone_id] = "mute"
            key_c = zone_id + "_c"
            nom_combat = "frigost" if zone_id in ZONES_FRIGOST else ("otomai" if zone_id in ZONES_OTOMAI else zone_id)
            if os.path.exists(os.path.join(DOSS_MUSIQUE, "1", f"1{nom_combat}combat.wav")):
                self.prefs_perso[key_c] = "1"
            elif os.path.exists(os.path.join(DOSS_MUSIQUE, "2", f"2{nom_combat}combat.wav")):
                self.prefs_perso[key_c] = "2"
            elif random_dispo:
                self.prefs_perso[key_c] = "aleatoire"
            else:
                self.prefs_perso[key_c] = "mute"

    def charger_configuration(self):
        os.makedirs(DOSS_LOG, exist_ok=True)
        if os.path.exists(FILE_CONFIG):
            try:
                with open(FILE_CONFIG, "r") as f:
                    data = json.load(f)
                    self.version_choisie.set(data.get("version_globale", "1"))
                    self.prefs_perso.update(data.get("zones", {}))
                    self.volume_sauvegarde = data.get("volume", 15)
                    self.zone_ocr_rect = data.get("zone_ocr_rect", "573x30+5+61")
                    pos_x = data.get("pos_x", None)
                    pos_y = data.get("pos_y", None)
                    if pos_x is not None and pos_y is not None:
                        self.root.geometry(f"+{pos_x}+{pos_y}")
            except: pass

    def sauvegarder_configuration(self):
        try:
            pos_x = self.root.winfo_rootx()
            pos_y = self.root.winfo_rooty()
        except:
            pos_x, pos_y = 100, 100
        data = {
            "version_globale": self.version_choisie.get(), 
            "zones": self.prefs_perso, 
            "volume": self.slider_vol.get(),
            "zone_ocr_rect": self.zone_ocr_rect,
            "pos_x": pos_x,
            "pos_y": pos_y
        }
        try:
            with open(FILE_CONFIG, "w") as f: 
                json.dump(data, f)
        except: 
            pass

    def actualiser_version(self):
        self.sauvegarder_configuration()
        if self.derniere_zone_detectee:
            self.musique_actuelle = "" 
            est_menu = (self.derniere_zone_detectee == "menu")
            self.gerer_musique(self.derniere_zone_detectee, est_menu)

    def ouvrir_config(self):
        if self.win_config is not None and self.win_config.winfo_exists():
            self.win_config.destroy(); self.win_config = None; return
            
        self.win_config = tk.Toplevel(self.root)

        def on_close_config():
            try:
                self.win_config.unbind_all("<MouseWheel>")
            except: pass
            self.win_config.destroy()
            self.win_config = None

        self.win_config.overrideredirect(True)
        self.win_config.configure(bg=BG_MAIN, highlightbackground=BORDER_COLOR, highlightthickness=1)
        self.win_config.attributes('-alpha', 0.95, '-topmost', True)
        self.appliquer_icone(self.win_config)

        self.root.update_idletasks()
        w_cfg, h_cfg, marge = 260, 460, 5
        mx, my, mw = self.root.winfo_rootx(), self.root.winfo_rooty(), self.root.winfo_width()
        sw = self.root.winfo_screenwidth()
        pos_x = (mx + mw + marge) if (mx + mw + marge + w_cfg) <= sw else (mx - w_cfg - marge)
        self.win_config.geometry(f"{w_cfg}x{h_cfg}+{pos_x}+{my}")

        header = tk.Frame(self.win_config, bg=BG_HEADER)
        header.pack(fill="x")
        
        lbl_title = tk.Label(header, text="Configuration Personnelle", font=("Arial", 8, "bold"), bg=BG_HEADER, fg=ACCENT_GREEN_CLAIR)
        lbl_title.pack(side="left", padx=8, pady=8)

        def reinitialiser_config():
            self.initialiser_prefs_auto()
            self.sauvegarder_configuration()
            on_close_config()
            self.ouvrir_config()

        lbl_close = tk.Label(header, text="✕", bg=BG_HEADER, fg=ACCENT_RED,
                             font=("Arial", 14), cursor="hand2")
        lbl_close.pack(side="right", padx=5)
        lbl_close.bind("<Button-1>", lambda e: on_close_config())

        lbl_reset = tk.Label(header, text="🔄", bg=BG_HEADER, fg=FG_LIGHT,
                             font=("Arial", 20), cursor="hand2")
        lbl_reset.pack(side="right", padx=4)
        lbl_reset.bind("<Button-1>", lambda e: reinitialiser_config())
        create_tooltip(lbl_reset, "Réinitialiser la config")

        def start_move_cfg(event): self.win_config._x, self.win_config._y = event.x, event.y
        def do_move_cfg(event):
            dx, dy = event.x - self.win_config._x, event.y - self.win_config._y
            self.win_config.geometry(f"+{self.win_config.winfo_x() + dx}+{self.win_config.winfo_y() + dy}")
        
        header.bind("<Button-1>", start_move_cfg); header.bind("<B1-Motion>", do_move_cfg)
        lbl_title.bind("<Button-1>", start_move_cfg); lbl_title.bind("<B1-Motion>", do_move_cfg)

        col_header = tk.Frame(self.win_config, bg=BG_SHADOW); col_header.pack(fill="x")
        tk.Label(col_header, text="ZONE", bg=BG_SHADOW, fg=FG_LIGHT, font=("Arial", 7, "bold"), width=18, anchor="w").pack(side="left", padx=15)
        
        container = tk.Frame(self.win_config, bg=BG_MAIN); container.pack(fill="both", expand=True)
        canvas = tk.Canvas(container, bg=BG_MAIN, highlightthickness=0)
        scroll = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=BG_MAIN)
        
        def _on_mouse(e):
            try:
                if canvas.winfo_exists():
                    canvas.yview_scroll(int(-1*(e.delta/120)), "units")
            except:
                try: self.win_config.unbind_all("<MouseWheel>")
                except: pass

        canvas.create_window((0,0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.bind_all("<MouseWheel>", _on_mouse)
        scroll.pack(side="right", fill="y"); canvas.pack(side="left", fill="both", expand=True)

        def get_btn_text(v, is_combat=False):
            if v == "mute": return "MUTE"
            if v == "aleatoire" and is_combat: return "RANDOM"
            return "1.29" if v == "1" else "2.0"

        def get_btn_fg(v):
            if v == "mute": return ACCENT_RED
            if v == "aleatoire": return "#FFA500"
            return ACCENT_GREEN if v == "1" else ACCENT_BLUE

        def toggle_pref(nom, key, btn):
            v_curr = self.prefs_perso.get(key, "1")
            is_combat = key.endswith("_c")
            suffixe = "combat" if is_combat else ""
            cycle = ["1", "2", "aleatoire", "mute"] if is_combat else ["1", "2", "mute"]
            idx = cycle.index(v_curr) if v_curr in cycle else 0
            # Substitutions via constantes globales
            for _ in range(len(cycle)):
                idx = (idx + 1) % len(cycle)
                nouvelle_v = cycle[idx]
                if nouvelle_v == "mute":
                    self.prefs_perso[key] = "mute"
                    btn.config(text="MUTE", fg=ACCENT_RED)
                    self.sauvegarder_configuration()
                    return
                if nouvelle_v == "aleatoire":
                    dossier_3 = os.path.join(DOSS_MUSIQUE, "3")
                    if os.path.exists(dossier_3) and any(f.endswith(".wav") for f in os.listdir(dossier_3)):
                        self.prefs_perso[key] = "aleatoire"
                        btn.config(text="RANDOM", fg="#FFA500")
                        self.sauvegarder_configuration()
                        return
                    continue
                nom_fichier = nom
                if is_combat and nom in ZONES_FRIGOST:
                    nom_fichier = "frigost"
                elif is_combat and nom in ZONES_OTOMAI:
                    nom_fichier = "otomai"
                elif not is_combat and nouvelle_v == "1" and nom in ZONES_PANDALA:
                    nom_fichier = "pandala"
                path = os.path.join(DOSS_MUSIQUE, nouvelle_v, f"{nouvelle_v}{nom_fichier}{suffixe}.wav")
                if os.path.exists(path):
                    self.prefs_perso[key] = nouvelle_v
                    btn.config(text="1.29" if nouvelle_v == "1" else "2.0",
                               fg=ACCENT_GREEN if nouvelle_v == "1" else ACCENT_BLUE)
                    self.sauvegarder_configuration()
                    return

        if not self.prefs_perso:
            self.prefs_perso = {z: "1" for z in NOMS_PROPRES.keys()}

        zones_uniques = sorted([z for z in self.prefs_perso.keys() if not z.endswith("_c")], 
                              key=lambda x: NOMS_PROPRES.get(x, x))

        for z_id in zones_uniques:
            row = tk.Frame(scroll_frame, bg=BG_MAIN); row.pack(fill="x", padx=5, pady=2)
            tk.Label(row, text=NOMS_PROPRES.get(z_id, z_id)[:18], bg=BG_MAIN, fg=FG_LIGHT, 
                     font=("Arial", 8), width=18, anchor="w").pack(side="left")
            v_e = self.prefs_perso.get(z_id, "1")
            b_e = tk.Button(row, text=get_btn_text(v_e), width=6, font=("Arial", 7, "bold"),
                            bg=BG_WIDGET, fg=get_btn_fg(v_e))
            b_e.config(command=lambda z=z_id, k=z_id, b=b_e: toggle_pref(z, k, b))
            b_e.pack(side="left", padx=2)
            key_c = z_id + "_c"
            if key_c not in self.prefs_perso: self.prefs_perso[key_c] = v_e
            v_c = self.prefs_perso.get(key_c, "1")
            b_c = tk.Button(row, text=get_btn_text(v_c, is_combat=True), width=6, font=("Arial", 7, "bold"),
                            bg="#444", fg=get_btn_fg(v_c))
            b_c.config(command=lambda z=z_id, k=key_c, b=b_c: toggle_pref(z, k, b))
            b_c.pack(side="left", padx=2)

        scroll_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def afficher_readme(self):
        if self.win_help is not None and self.win_help.winfo_exists():
            self.win_help.destroy()
            self.win_help = None
            return

        self.win_help = tk.Toplevel(self.root)
        self.win_help.overrideredirect(True)
        self.win_help.configure(bg=BG_MAIN, highlightbackground=BORDER_COLOR, highlightthickness=1)
        self.win_help.attributes('-alpha', 0.95, '-topmost', True)
        self.appliquer_icone(self.win_help)

        self.root.update_idletasks()
        w_help, h_help, marge = 450, 500, 5
        mx, my, mw = self.root.winfo_rootx(), self.root.winfo_rooty(), self.root.winfo_width()
        sw = self.root.winfo_screenwidth()
        pos_x = (mx + mw + marge) if (mx + mw + marge + w_help) <= sw else (mx - w_help - marge)
        self.win_help.geometry(f"{w_help}x{h_help}+{pos_x}+{my}")

        head = tk.Frame(self.win_help, bg=BG_HEADER)
        head.pack(fill="x")
        lbl_title = tk.Label(head, text="INFORMATIONS & AIDE", font=("Arial", 8, "bold"), 
                             bg=BG_HEADER, fg=ACCENT_GREEN_CLAIR)
        lbl_title.pack(side="left", padx=10, pady=8)

        def start_move_help(event): self.win_help._x, self.win_help._y = event.x, event.y
        def do_move_help(event):
            dx, dy = event.x - self.win_help._x, event.y - self.win_help._y
            self.win_help.geometry(f"+{self.win_help.winfo_x() + dx}+{self.win_help.winfo_y() + dy}")
        head.bind("<Button-1>", start_move_help)
        head.bind("<B1-Motion>", do_move_help)
        lbl_title.bind("<Button-1>", start_move_help)
        lbl_title.bind("<B1-Motion>", do_move_help)

        tk.Button(head, text="✕", command=self.win_help.destroy, 
                  bg=BG_WIDGET, fg=ACCENT_RED, font=("Arial", 8, "bold"), 
                  relief=tk.RAISED, borderwidth=2, padx=10).pack(side="right", padx=5, pady=5)

        path_readme = os.path.join(BASE_PATH, "READ ME.txt")
        contenu = "Fichier READ ME.txt introuvable."
        if os.path.exists(path_readme):
            for enc in ["utf-8", "ansi"]:
                try:
                    with open(path_readme, "r", encoding=enc) as f:
                        contenu = f.read()
                        break
                except: continue

        f_txt = tk.Frame(self.win_help, bg=BG_MAIN)
        f_txt.pack(fill="both", expand=True, padx=10, pady=10)
        area = tk.Text(f_txt, bg="#1a1a1a", fg=FG_LIGHT, font=("Consolas", 9), 
                       padx=10, pady=10, wrap="word", borderwidth=0)
        area.insert("1.0", contenu)
        area.config(state="disabled")
        area.pack(fill="both", expand=True)

    def quitter(self): 
        self.sauvegarder_configuration()
        self.sauvegarder_log()
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except:
            pass
        keyboard.unhook_all()
        self.root.destroy()
        os._exit(0)

    def demarrer_deplacement(self, event):
        if "button" not in str(event.widget).lower() and "scale" not in str(event.widget).lower():
            self.drag_allowed = True; self.x, self.y = event.x, event.y
        else: self.drag_allowed = False

    def deplacer_fenetre(self, event):
        if hasattr(self, 'drag_allowed') and self.drag_allowed:
            dx, dy = event.x - self.x, event.y - self.y
            self.root.geometry(f"+{self.root.winfo_x() + dx}+{self.root.winfo_y() + dy}")

    def ajuster_volume(self, val):
        vol = float(val) / 100
        try:
            pygame.mixer.music.set_volume(vol)
            self.volume_sauvegarde = int(val)
            self.sauvegarder_configuration()
        except:
            pass

    def toggle(self):
        self.actif = not self.actif
        if self.actif:
            self.label_status.config(text="STATUT : ACTIF", fg=ACCENT_GREEN)
            self.musique_actuelle = ""
            if self.derniere_zone_detectee:
                self.gerer_musique(self.derniere_zone_detectee, self.derniere_zone_detectee == "menu")
            else:
                self.jouer_fichier(os.path.join(DOSS_MUSIQUE, "menu.wav"), "Accueil")
        else:
            self.label_status.config(text="STATUT : EN PAUSE", fg=ACCENT_RED)
            pygame.mixer.music.fadeout(300)
            self.musique_actuelle = ""
            self.label_music.config(text="Silencieux")

    def jouer_fichier(self, path, nom_display):
        if not os.path.exists(path):
            self.label_music.config(text="⚠ Fichier manquant", fg=ACCENT_RED)
            print(f"Fichier introuvable : {path}")
            return
        if self.musique_actuelle != path:
            try:
                pygame.mixer.music.fadeout(400)
                pygame.mixer.music.load(path)
                pygame.mixer.music.play(loops=-1, fade_ms=250)
                self.musique_actuelle = path
                couleur = ACCENT_RED if self.en_combat else ACCENT_GREEN_CLAIR
                self.label_music.config(text=nom_display, fg=couleur)
            except Exception as e:
                self.musique_actuelle = ""
                self.label_music.config(text="⚠ Erreur lecture", fg=ACCENT_RED)
                print(f"Erreur Pygame : {e}")

    def gerer_musique(self, nom, is_menu_special, combat_actuel=None):
        mode = self.version_choisie.get()
        self.en_combat = combat_actuel if combat_actuel is not None else self.detecter_combat()

        if not nom and not is_menu_special:
            if self.en_combat:
                self.jouer_musique_aleatoire_combat("Combat (Zone Inconnue)")
            else:
                self.jouer_musique_aleatoire_exploration("Exploration (Zone Inconnue)")
            return

        if is_menu_special:
            self.jouer_fichier(os.path.join(DOSS_MUSIQUE, "menu.wav"), "Démarrage")
            return

        display = NOMS_PROPRES.get(nom, nom.capitalize())
        if mode == "3":
            v_pref = self.prefs_perso.get(nom + "_c" if self.en_combat else nom, "1")
        else:
            v_pref = mode

        if v_pref == "mute":
            pygame.mixer.music.fadeout(500)
            self.musique_actuelle = "mute"
            label_combat = " (COMBAT)" if self.en_combat else ""
            self.label_music.config(text=f"{display}{label_combat} MUTE", fg="#888888")
            return

        if v_pref == "aleatoire" and self.en_combat:
            self.jouer_musique_aleatoire_combat(f"{display} (Combat Aléatoire)")
            return

        nom_fichier = nom
        if v_pref == "1" and nom in ZONES_PANDALA:
            nom_fichier = "pandala"
        if self.en_combat and nom in ZONES_FRIGOST:
            nom_fichier = "frigost"
        if self.en_combat and nom in ZONES_OTOMAI:
            nom_fichier = "otomai"

        v_alt = "2" if v_pref == "1" else "1"
        suffixe = "combat" if self.en_combat else ""

        p1 = os.path.join(DOSS_MUSIQUE, v_pref, f"{v_pref}{nom_fichier}{suffixe}.wav")
        p2 = os.path.join(DOSS_MUSIQUE, v_alt, f"{v_alt}{nom_fichier}{suffixe}.wav")
        label_combat = " (COMBAT)" if self.en_combat else ""

        def get_version_label(v, f):
            if v == "2" and f == "wabbitcombat":
                return "WAKFU"
            return "1.29" if v == "1" else "2.0"

        if os.path.exists(p1):
            ver_txt = get_version_label(v_pref, f"{nom_fichier}{suffixe}")
            self.jouer_fichier(p1, f"{display}{label_combat} {ver_txt}")
        elif os.path.exists(p2):
            ver_txt = get_version_label(v_alt, f"{nom_fichier}{suffixe}")
            self.jouer_fichier(p2, f"{display}{label_combat} {ver_txt}")
        elif self.en_combat:
            self.jouer_musique_aleatoire_combat(f"{display} (Combat Aléatoire)")

    def jouer_musique_aleatoire_combat(self, label_info):
        dossier_3 = os.path.join(DOSS_MUSIQUE, "3")
        if os.path.exists(dossier_3):
            sons = [f for f in os.listdir(dossier_3) if f.endswith(".wav")]
            if sons:
                choix = random.choice(sons)
                self.jouer_fichier(os.path.join(dossier_3, choix), f"{label_info} : {choix}")

    def jouer_musique_aleatoire_exploration(self, label_info):
        v = self.version_choisie.get()
        if v == "3": v = "1"
        dossier_v = os.path.join(DOSS_MUSIQUE, v)
        if os.path.exists(dossier_v):
            sons = [f for f in os.listdir(dossier_v) if f.endswith(".wav") and "combat" not in f.lower()]
            if sons:
                choix = random.choice(sons)
                self.jouer_fichier(os.path.join(dossier_v, choix), f"{label_info} : {choix}")

    def boucle_scan(self):
        self.dernier_etat_combat = False
        self.derniere_zone_detectee = ""
        from PIL import ImageGrab

        base_detections = [
            ("havre-sac", "havresac", False), ("abraknydes", "abra", False), ("gelées", "gelée", False), ("abraknydés", "abra", False), 
            ("bworks", "bwork", False), ("gobelins", "bwork", False), ("château d'amakna", "chamakna", False), 
            ("marécages d'amakna", "ankmarecage", False), ("marécages nauséab", "marecage", False), 
            ("marécages sans fond", "marecage", False), ("dragoeufs", "drag", False), 
            ("rivage sufokien", "plageamakna", False), ("coin des boos", "plageamakna", False), ("coin des bôos", "plageamakna", False), ("coin de boo", "plageamakna", False), 
            ("côte d'asse", "plageamakna", False), ("kartonpath", "karton", False),
            ("basse des craqueleurs", "mbcraque", False), ("amakna (montagne", "mcraque", False), 
            ("des bouftous", "amakna", False), ("porcos", "porcos", False), ("milifutaie", "amakna", False), 
            ("scarafeuilles", "amakna", False), ("forêt d'amakna", "amakna", False), 
            ("bord de la forêt maléfique", "amakna", False), ("territoire des bandits", "amakna", False), 
            ("boulgoure", "amakna", False), ("ingalsse", "amakna", False), ("campagne d'amakna", "amakna", False), 
            ("village d'amakna", "amakna", False), ("ivière kaw", "plageamakna", False), 
            ("madrestam", "plageamakna", False), ("cryptes du cimetière", "cimetière", False), 
            ("amakna (cimetière)", "cimetière", False), ("taverne", "taverne", False), 
            ("cimetière d'astrub", "cimetière", False), ("prairies d'astrub", "pastrub", False), 
            ("carrière d'astrub", "astrub", False), ("cité d'astrub", "astrub", False), 
            ("forêt d'astrub", "fastrubkoala", False), ("champs d'astrub", "pastrub", False), 
            ("tainéla", "astrub", False), ("calanques d'astrub", "pastrub", False), 
            ("de la milice", "astrub", False), 
            ("temple iop", "tiop", False), ("temple lop", "tiop", False), ("temple crâ", "tcra", False), ("temple cra", "tcra", False), ("temple osamodas", "tosamodas", False), ("temple féca", "tfeca", False), ("temple feca", "tfeca", False),
            ("temple enutrof", "tenutrof", False), ("temple sram", "tsram", False), 
            ("temple xélor", "txelor", False), ("temple xelor", "txelor", False), ("temple écaflip", "tecaflip", False), ("temple ecaflip", "tecaflip", False),
            ("temple eniripsa", "teniripsa", False), 
            ("temple pandawa", "tpandawa", False), ("temple sadida", "tsadida", False), 
            ("temple sacrieur", "tsacrieur", False),
            ("temple roublard", "troublard", False), ("temple zobal", "tzobal", False), 
            ("temple steamer", "tsteamer", False), ("temple eliotrope", "teliotrop", False),
            ("temple ouginak", "touginak", False), ("meute", "touginak", False),
            ("temple huppermage", "thuppermage", False), ("île de rok", "thuppermage", False),
            ("incarnam", "incarnam", False), ("temple des douze", "astrub", False), 
            ("bonta", "bonta", False), ("brâkmar", "brakmar", False), ("brâäkmar", "brakmar", False), ("bräkmar", "brakmar", False), ("braàkmar", "brakmar", False), ("bràkmar", "brakmar", False), ("bràakmar", "brakmar", False), ("brakmar", "brakmar", False), ("ire du trool", "trool", False), 
            ("minotoror", "mino", False), ("moon", "moon", False), ("wabbits", "wabbit", False), 
            ("sidimote", "sidimote", False), ("baie de sufokia (sufokia)", "sufokia", False), 
            ("port de givre", "portdegivre", False), ("mer kantil", "portdegivre", False), ("bourgade", "bourgade", False), ("poo nt de givne","portdegivre", False), ("port.detgivre","portdegivre", False), ("port.detoivrc","portdegivre", False), 
            ("champs de glace", "bourgade", False), ("champs dé glace", "bourgade", False), ("champs detglace", "bourgade", False), ("lac gelé", "frigost", False), ("lae gelé", "frigost", False), ("lac gele", "frigost", False), 
            ("des pins perdus", "forpinperdu", False), ("crocs de verre", "frigost", False), ("honetfdesipins perdus", "forpinperdu", False), ("horetidesipinsipendus", "forpinperdu", False), ("foretidestpinstperdus", "forpinperdu", False), ("forêt despins perdus", "forpinperdu", False), ("forêt destpins perdus", "forpinperdu", False),
            ("forêt dés pins perdus", "forpinperdu", False), ("forêt dès pins pendu", "forpinperdu", False), ("forét des pins pendu", "forpinperdu", False), ("honetadestpinsipendu", "forpinperdu", False),
            ("frigost (berceau", "larmeberceau", False), ("ouronigride", "larmeberceau", False), 
            ("crevasse perge", "creperg", False), ("forêt pétrifiée", "forpet", False), 
            ("village enseveli", "bourgade", False), ("martegel", "martegel", False), 
            ("torrideau", "ruchglours", False), ("gloursons", "ruchglours", False), 
            ("remparts à vent", "rempvent", False), ("tannerie écarlate", "rempvent", False), 
            ("jardins d'hiver", "jardhiv", False), ("bastion des froides légions", "jardhiv", False), 
            ("entrée du château de harebourg", "frigost", False), ("clepsydre", "tourclep", False), 
            ("caserne du jour", "casjourfin", False), ("salbatroces", "frigost", False), 
            ("sakaï", "frigost", False), ("cania", "cania", False), ("canïa", "cania", False), ("cani a", "cania", False), ("cani é", "cania", False), ("village de pandala", "vpandala", False), ("village de pañndala", "vpandala", False), ("village de pandalà", "vpandala", False), 
            ("akwadala", "akwadala", False), ("akwadäla", "akwadala", False), ("akwädala", "akwadala", False), ("terrdala", "terrdala", False), ("plantala", "plantala", False), 
            ("aerdala", "aerdala", False), ("feudala", "feudala", False), ("grobe", "grobe", False), 
            ("wukin", "pandala", False), ("lage de la canopée", "vcanop", False), ("lage deda canô", "vcanop", False), ("lage dedmcanop", "vcanop", False), ("lage deds{cano", "vcanop", False), 
            ("cloaque d'amakna", "cavemine", False), ("égouts d'astrub", "cavemine", False), 
            ("souterrains d'astrub", "cavemine", False), ("mine", "cavemine", False), 
            ("lage des zoths", "vzoth", False), ("lage désioths", "vzoth", False), ("tourbière", "tourboto", False), 
            ("age de corail", "otomai", False), ("plaines herbeuses", "otomai", False), 
            ("village des plaines", "otomai", False), ("jungle obscure", "otomai", False), 
            ("lage de l'arbre hakam", "hakam", False), ("tronc de l'arbre hakam", "hakam", False), 
            ("village côtier", "otomai", False), ("île des naufragés", "otomai", False), 
            ("dimension obscure", "dimobs", False), ("ecaflipus", "ecaflipus", False), 
            ("enutrosor", "enutrosor", False), ("srambad", "srambad", False), 
            ("xélorium", "xelorium", False), ("village des éleveurs", "vkoalak", False), ("enclos", "vkoalak", False), ("village des éléveürs", "vkoalak", False),
            ("territoire des drago", "koalak", False), ("lacs enchantés", "koalak", False), 
            ("forêt de kaliptus", "koalak", False), ("canyon sauvage", "koalak", False), 
            ("vallée de la morh'kitu", "mkoalak", False),("brigandins", "vzoth", False),
            ("de kerubim", "astrub", False),("dragon cochon", "porcos", False),
            ("vulkania", "vulkania", False),("nowel", "nowel", False),
            ("dale du dark vla", "dedaledv", False),("orée enchantée", "oreeenchant", False),
            ("bibliotemple", "bibli", False),("osavora", "osavora", False),
            ("première salle", "donjon", False),("deuxième salle", "donjon", False),("troisième salle", "donjon", False),("salle annexe", "donjon", False),("quatrième salle", "donjon", False),("cinquième salle", "donjon", False),("- sortie", "donjon", False),("sixième salle", "donjon", False),
            ("septième salle", "donjon", False),("huitième salle", "donjon", False),("neuvième salle", "donjon", False),("dixième salle", "donjon", False),("onzième salle", "donjon", False),("douzième salle", "donjon", False),("treizième salle", "donjon", False),
            ("yageurs dimensi", "cania", False),("kanojedo", "amakna", False),("ingloriom", "ingloriom", False)
        ]

        while True:
            if self.actif:
                try:
                    screenshot_full = ImageGrab.grab(all_screens=True)
                    combat_actuel = self.detecter_combat(screenshot=screenshot_full)
                    
                    parts = self.zone_ocr_rect.replace('x', '+').split('+')
                    w, h, x, y = map(int, parts)
                    cap = ImageGrab.grab(bbox=(x, y, x + w, y + h), all_screens=True)
                    cap = cap.convert('L').resize((cap.width * 3, cap.height * 3), Image.Resampling.LANCZOS)
                    cap = cap.point(lambda p: 0 if p > 225 else 300)
                    txt = pytesseract.image_to_string(cap, lang='fra', config='--psm 7').strip().lower()
                    #cap.save("debug_ocr.png")
                    if self.win_ocr_debug is not None and self.win_ocr_debug.winfo_exists():
                        ts = time.strftime("%H:%M:%S")
                        zone_display = NOMS_PROPRES.get(self.derniere_zone_detectee, self.derniere_zone_detectee or "--")
                        combat_display = "OUI" if combat_actuel else "NON"
                        zone_log = self.log_data.get(self.derniere_zone_detectee, {})
                        historique = zone_log.get("historique", [])
                        total = len(historique)
                        coherents = sum(historique)
                        pct = f"{coherents / total * 100:.1f}%" if total > 0 else "--%"
                        fiab_couleur = "#00ff99" if total > 0 and coherents / total >= 0.8 else ("#FFA500" if total > 0 and coherents / total >= 0.5 else "#ef5350")
                        self.win_ocr_debug.after(0, lambda t=txt, s=ts, z=zone_display, c=combat_display, p=pct, fc=fiab_couleur: (
                            self.lbl_ocr_debug.config(text=t if t else "(rien détecté)"),
                            self.lbl_ocr_zone.config(text=f"Zone : {z} | Combat : {c}"),
                            self.lbl_ocr_fiabilite.config(text=f"Fiabilité zone : {p}", fg=fc),
                            self.lbl_ocr_time.config(text=f"Dernier scan : {s}")
                        ))

                    # Filtrer les textes OCR non significatifs (trop courts ou mots parasites)
                    MOTS_PARASITES = {"de", "du", "la", "le", "les", "des", "un", "une", "en", "et", "il", "a"}
                    txt_valide = len(txt) > 3 and txt.strip() not in MOTS_PARASITES

                    trouve_zone = False
                    
                    if txt and txt_valide:
                        for mot, fich, is_menu in base_detections:
                            if "temple" in mot:
                                condition_met = (mot in txt)
                            elif mot in txt:
                                condition_met = True
                            else:
                                condition_met = SequenceMatcher(None, txt, mot).ratio() > 0.8
                            
                            if condition_met:
                                if fich != self.derniere_zone_detectee or combat_actuel != self.dernier_etat_combat:
                                    if fich != self.derniere_zone_detectee:
                                        self.nettoyer_erreurs_transition(self.derniere_zone_detectee, fich, base_detections)
                                    self.en_combat = combat_actuel
                                    self.derniere_zone_detectee = fich
                                    self.dernier_etat_combat = combat_actuel
                                    self.gerer_musique(fich, is_menu, combat_actuel=combat_actuel)
                                self.enregistrer_detection(fich, succes=True, txt_ocr="")
                                trouve_zone = True
                                break
                        
                        if not trouve_zone and self.derniere_zone_detectee:
                            self.enregistrer_detection(self.derniere_zone_detectee, succes=False, txt_ocr=txt)
                    elif txt and not txt_valide and self.derniere_zone_detectee:
                        pass  # Texte parasite, on ignore complètement

                    if not trouve_zone:
                        if combat_actuel != self.dernier_etat_combat:
                            self.en_combat = combat_actuel
                            self.dernier_etat_combat = combat_actuel
                            self.gerer_musique(self.derniere_zone_detectee, False, combat_actuel=combat_actuel)

                except Exception as e:
                    print(f"Erreur Scan: {e}")

            time.sleep(0.4)

if __name__ == "__main__":
    root = tk.Tk(); app = DofusMusicApp(root); root.mainloop()
