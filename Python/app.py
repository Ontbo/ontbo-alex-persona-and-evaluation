import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import csv
import pathlib
import json
import random
import argparse
import sys

STIMULI_PATH = pathlib.Path("stimuli.json")


def nettoyer_texte(texte):
    return texte.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')


class ExperimentApp(tk.Tk):
    def __init__(self, ordre="aleatoire"):
        super().__init__()

        self.ordre = ordre
        self.title("Expérience Oui / Non")
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.destroy())

        self.current_index = -1
        self.responses = []
        self.stimuli = self.charger_stimuli()
        self.csv_path = None
        self.start_time_str = None
        self.table_frame = None

        self.top_frame = tk.Frame(self)
        self.top_frame.pack(side="top", fill="both", expand=True)

        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.pack(side="bottom", fill="x", pady=20)

        self.canvas = tk.Canvas(self.top_frame)
        self.scrollbar = tk.Scrollbar(self.top_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

        self.lbl_text = tk.Label(
            self.scrollable_frame,
            text="",
            font=("Noto Sans JP", 16),
            wraplength=1800,
            justify="left",
            anchor="nw"
        )
        self.lbl_text.pack(padx=40, pady=40)

        self.btn_left = tk.Button(self.bottom_frame, text="", width=30)
        self.btn_right = tk.Button(self.bottom_frame, text="", width=30)

        self.show_start_page()

    def _on_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")

    def update_scroll_visibility(self):
        self.update_idletasks()
        content_height = self.scrollable_frame.winfo_height()
        visible_height = self.canvas.winfo_height()

        if content_height > visible_height:
            self.scrollbar.pack(side="right", fill="y")
        else:
            self.scrollbar.pack_forget()

    def charger_stimuli(self):
        if not STIMULI_PATH.exists():
            messagebox.showerror("Erreur", f"Fichier {STIMULI_PATH} introuvable.")
            self.destroy()
            sys.exit(1)

        with STIMULI_PATH.open(encoding="utf-8") as f:
            data = json.load(f)

        for item in data:
            if "nom" not in item or "valeur" not in item:
                raise ValueError("Chaque stimulus doit avoir un champ 'nom' et 'valeur'.")

        return data

    def show_start_page(self):
        self.clear_window()

        consignes = (
            "Bienvenue et merci de participer !\n\n"
            "Vous allez lire une série d'énoncés. "
            "Pour chacun, cliquez sur « Oui » s'il vous paraît correct, "
            "ou « Non » s'il vous paraît incorrect.\n\n"
            "Cliquez sur « Continuer » pour lire l'introduction."
        )
        self.lbl_text.config(text=nettoyer_texte(consignes))
        self.canvas.yview_moveto(0)
        self.update_scroll_visibility()

        self.btn_right.config(text="Continuer", width=30, command=self.show_intro_page)
        self.btn_right.pack(side="right", padx=20)

    def show_intro_page(self):
        self.clear_window()

        intro = (
            "Dans un instant, l'expérimentation débutera.\n"
            "Répondez de manière aussi précise que possible.\n\n"
            "Cliquez sur « Commencer l'expérimentation » dès que vous êtes prêt·e."
        )
        self.lbl_text.config(text=nettoyer_texte(intro))
        self.canvas.yview_moveto(0)
        self.update_scroll_visibility()

        self.btn_right.config(
            text="Commencer l'expérimentation",
            width=30,
            command=self.start_trials
        )
        self.btn_right.pack(side="right", padx=20)

    def start_trials(self):
        self.start_time_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.csv_path = pathlib.Path(f"reponses_{self.start_time_str}.csv")

        if self.ordre == "aleatoire":
            random.shuffle(self.stimuli)

        self.current_index = 0
        self.show_trial_page()

    def show_trial_page(self):
        self.clear_window()

        if self.current_index >= len(self.stimuli):
            self.end_experiment()
            return

        stimulus = self.stimuli[self.current_index]
        self.lbl_text.config(text="")

        if isinstance(stimulus["valeur"], dict) and stimulus["valeur"].get("type") == "tableau":
            self.afficher_tableau(stimulus["valeur"])
        else:
            texte = nettoyer_texte(str(stimulus["valeur"]))
            self.lbl_text.config(text=texte)

        self.canvas.yview_moveto(0)
        self.update_scroll_visibility()

        self.btn_left.config(text="Oui", width=30, command=lambda: self.record_response("Oui"))
        self.btn_right.config(text="Non", width=30, command=lambda: self.record_response("Non"))
        self.btn_left.pack(side="left", padx=60)
        self.btn_right.pack(side="right", padx=60)

    def afficher_tableau(self, table_data):
        colonnes = table_data.get("colonnes", [])
        lignes = table_data.get("lignes", [])

        self.table_frame = tk.Frame(self.scrollable_frame)
        self.table_frame.pack(pady=40)

        for j, col in enumerate(colonnes):
            tk.Label(
                self.table_frame, text=col, font=("Noto Sans JP", 14, "bold"),
                borderwidth=1, relief="solid", padx=10, pady=5
            ).grid(row=0, column=j, sticky="nsew")

        for i, ligne in enumerate(lignes, start=1):
            for j, cell in enumerate(ligne):
                tk.Label(
                    self.table_frame, text=str(cell), font=("Noto Sans JP", 14),
                    borderwidth=1, relief="solid", padx=10, pady=5
                ).grid(row=i, column=j, sticky="nsew")

    def end_experiment(self):
        self.save_responses()
        self.clear_window()

        message = "Expérience terminée.\n\nMerci de votre participation !"
        self.lbl_text.config(text=nettoyer_texte(message))
        self.canvas.yview_moveto(0)
        self.update_scroll_visibility()

        self.btn_right.config(text="Quitter", width=30, command=self.destroy)
        self.btn_right.pack(side="right", padx=20)

    def record_response(self, answer):
        stimulus = self.stimuli[self.current_index]
        nom = stimulus.get("nom", "")
        agent = stimulus.get("agent", "")
        timestamp = datetime.now().isoformat(timespec="seconds")

        self.responses.append({
            "nom": nom,
            "agent": agent,
            "reponse": answer,
            "horodatage": timestamp,
        })

        self.current_index += 1
        self.show_trial_page()

    def save_responses(self):
        header = ["nom", "agent", "reponse", "horodatage"]
        new_file = not self.csv_path.exists()

        with self.csv_path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=header)
            if new_file:
                writer.writeheader()
            writer.writerows(self.responses)

        messagebox.showinfo("Sauvegarde", f"Réponses enregistrées dans :\n{self.csv_path.resolve()}")

    def clear_window(self):
        self.btn_left.pack_forget()
        self.btn_right.pack_forget()
        self.lbl_text.config(text="")
        if self.table_frame:
            self.table_frame.destroy()
            self.table_frame = None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lance une expérimentation Oui/Non.")
    parser.add_argument(
        "--ordre",
        choices=["aleatoire", "fixe"],
        default="aleatoire",
        help="Ordre de présentation des stimuli (par défaut : aleatoire)."
    )
    args = parser.parse_args()

    app = ExperimentApp(ordre=args.ordre)
    app.mainloop()
