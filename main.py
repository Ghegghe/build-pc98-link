import os
import sys
from pathlib import Path
from PIL import Image
import subprocess
import tomllib
import ctypes


# --- CARICAMENTO CONFIGURAZIONE ---
def load_config():
    # Determina la cartella dove si trova l'eseguibile o lo script
    if getattr(sys, "frozen", False):
        # Se è un .exe, usa il percorso dell'eseguibile
        base_path = Path(sys.executable).parent
    else:
        # Se è uno script .py, usa il percorso del file sorgente
        base_path = Path(__file__).parent

    config_path = base_path / "config.toml"

    if not config_path.exists():
        msg = f"Errore critico: File {config_path} non trovato!"
        # Mostra una finestra di errore Windows
        ctypes.windll.user32.MessageBoxW(0, msg, "Errore Configurazione", 0x10)
        sys.exit(1)

    with open(config_path, "rb") as f:
        config = tomllib.load(f)

    return config["SETTINGS"]


# Carichiamo le impostazioni globali
SETTINGS = load_config()
DOSBOX_PATH = SETTINGS.get("dosbox_path")
CONF_CONTENT = SETTINGS.get("conf_content")
DESKTOP_PATH = Path(os.path.join(os.environ["USERPROFILE"], "Desktop"))
CONFIG_NAME = "game.conf"


def create_shortcut(target_exe, arguments, shortcut_path, icon_path):
    """Crea un collegamento Windows via PowerShell"""
    ps_command = f"""
    $W = New-Object -ComObject WScript.Shell;
    $S = $W.CreateShortcut('{shortcut_path}');
    $S.TargetPath = '{target_exe}';
    $S.Arguments = '{arguments}';
    $S.IconLocation = '{icon_path}';
    $S.Save();
    """
    subprocess.run(["powershell", "-Command", ps_command], capture_output=True)


def process_folder(folder_path):
    folder = Path(folder_path).absolute()
    if not folder.is_dir():
        print(f"Errore: {folder} non è una cartella.")
        return

    print(f"--- Elaborazione: {folder.name} ---")

    # 1. Trova il file .hdi
    hdi_files = list(folder.glob("*.hdi"))
    if not hdi_files:
        print("  [!] Nessun file .hdi trovato.")
        return
    hdi_file = hdi_files[0]

    # 2. Gestione Immagine (Ridimensionamento con proporzioni e conversione ICO)
    icon_path = folder / "icon.ico"
    cover_found = False
    for ext in ["*.jpg", "*.jpeg", "*.png", "*.webp", "*.bmp"]:
        covers = list(folder.glob(ext))
        if covers:
            try:
                img = Image.open(covers[0]).convert("RGBA")

                # --- LOGICA DI RESIZE (Mantenere Aspect Ratio) ---
                size = 256
                # Calcoliamo il rapporto per non stretchare
                img.thumbnail((size, size), Image.Resampling.LANCZOS)

                # Creiamo uno sfondo quadrato trasparente
                new_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))

                # Incolliamo l'immagine al centro
                upper_left = ((size - img.size[0]) // 2, (size - img.size[1]) // 2)
                new_img.paste(img, upper_left)

                # Salvataggio
                new_img.save(
                    icon_path,
                    format="ICO",
                    sizes=[(256, 256), (128, 128), (64, 64), (32, 32)],
                )
                # -------------------------------------------------

                cover_found = True
                print(f"  [+] Icona creata correttamente da {covers[0].name}")
                break
            except Exception as e:
                print(f"  [!] Errore immagine: {e}")

    if not cover_found:
        icon_path = ""

    # 3. Crea il file .conf (CORRETTO SECONDO WIKI DOSBOX-X)
    conf_file = folder / CONFIG_NAME
    # Usiamo .as_posix() per avere i percorsi con / che DOSBox digerisce meglio
    hdi_posix = hdi_file.as_posix()

    conf_content = (
        CONF_CONTENT
        + f"""
[autoexec]
IMGMOUNT C "{hdi_posix}"
C:
BOOT
"""
    )
    with open(
        conf_file, "w", encoding="utf-8"
    ) as config:  # <--- AGGIUNTO encoding="utf-8"
        config.write(conf_content)
    print("  [+] File .conf generato.")

    # 4. Crea il collegamento sul Desktop
    shortcut_name = f"{folder.name}.lnk"
    shortcut_full_path = DESKTOP_PATH / shortcut_name
    args = f'-conf "{conf_file.as_posix()}"'

    create_shortcut(DOSBOX_PATH, args, str(shortcut_full_path), str(icon_path))
    print("  [OK] Collegamento creato sul Desktop!")


if __name__ == "__main__":
    folders = sys.argv[1:]
    if not folders:
        ctypes.windll.user32.MessageBoxW(
            0,
            "Trascina una o più cartelle sull'icona per creare i collegamenti.",
            "Istruzioni",
            0x40,
        )
    else:
        for f in folders:
            process_folder(f)
        ctypes.windll.user32.MessageBoxW(
            0, "Elaborazione completata con successo!", "Fine", 0x40
        )
