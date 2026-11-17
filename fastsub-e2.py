import tkinter as tk
from tkinter import filedialog, messagebox
import json
import datetime
import os


def segundos_para_srt(segundos):
    hora_formatada = str(datetime.timedelta(seconds=float(segundos)))
    if '.' in hora_formatada:
        tempo, milisegundos = hora_formatada.split('.')
        milisegundos = milisegundos[:3].ljust(3, '0')
    else:
        tempo = hora_formatada
        milisegundos = "000"

    if len(tempo.split(':')[0]) == 1:
        tempo = "0" + tempo
    return f"{tempo},{milisegundos}"


class FastSubMotor:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 FastSub Core - Motor de Regras")
        self.root.geometry("600x600")  # Aumentei um pouco para caber a nova regra
        self.root.configure(padx=20, pady=20, bg="#1e1e1e")

        self.caminho_json = None

        fonte_titulo = ("Segoe UI", 12, "bold")
        fonte_texto = ("Segoe UI", 10)
        bg_color = "#1e1e1e"
        fg_color = "#d4d4d4"

        # --- SEÇÃO 1: ARQUIVO ---
        tk.Label(root, text="1️⃣ Fonte de Dados:", font=fonte_titulo, bg=bg_color, fg="white").pack(anchor="w",
                                                                                                    pady=(0, 5))

        self.btn_selecionar = tk.Button(root, text="📂 Selecionar Arquivo JSON", font=fonte_texto, bg="#333333",
                                        fg="white", cursor="hand2", command=self.selecionar_arquivo)
        self.btn_selecionar.pack(fill="x", ipady=5)

        self.lbl_arquivo = tk.Label(root, text="Nenhum arquivo selecionado.", font=("Consolas", 9), bg=bg_color,
                                    fg="#888888")
        self.lbl_arquivo.pack(anchor="w", pady=(5, 15))

        # --- SEÇÃO 2: REGRAS ---
        tk.Label(root, text="2️⃣ Parâmetros de Ritmo:", font=fonte_titulo, bg=bg_color, fg="white").pack(anchor="w",
                                                                                                         pady=(0, 10))

        frame_regras = tk.Frame(root, bg=bg_color)
        frame_regras.pack(fill="x", pady=5)

        # Regra 1: CPL
        tk.Label(frame_regras, text="Limite de Caracteres por Linha (CPL):", font=fonte_texto, bg=bg_color,
                 fg=fg_color).grid(row=0, column=0, sticky="w", pady=8)
        self.input_cpl = tk.Entry(frame_regras, font=fonte_texto, width=10, justify="center")
        self.input_cpl.insert(0, "35")
        self.input_cpl.grid(row=0, column=1, padx=10)

        # Regra 2: GAP
        tk.Label(frame_regras, text="Pausa Máxima de Fôlego (Segundos):", font=fonte_texto, bg=bg_color,
                 fg=fg_color).grid(row=1, column=0, sticky="w", pady=8)
        self.input_gap = tk.Entry(frame_regras, font=fonte_texto, width=10, justify="center")
        self.input_gap.insert(0, "0.4")
        self.input_gap.grid(row=1, column=1, padx=10)

        # Regra 3: Max Words
        tk.Label(frame_regras, text="Máximo de Palavras por Bloco (0 = Infinito):", font=fonte_texto, bg=bg_color,
                 fg=fg_color).grid(row=2, column=0, sticky="w", pady=8)
        self.input_words = tk.Entry(frame_regras, font=fonte_texto, width=10, justify="center")
        self.input_words.insert(0, "0")
        self.input_words.grid(row=2, column=1, padx=10)

        # Regra 4: Hang Time (NOVA REGRA)
        tk.Label(frame_regras, text="Tempo Extra de Leitura (Hang Time - Seg):", font=fonte_texto, bg=bg_color,
                 fg=fg_color).grid(row=3, column=0, sticky="w", pady=8)
        self.input_hang = tk.Entry(frame_regras, font=fonte_texto, width=10, justify="center")
        self.input_hang.insert(0, "0.3")  # Vai estender as legendas curtas em até 0.3s se houver espaço
        self.input_hang.grid(row=3, column=1, padx=10)

        # Regra 5: Interrogação
        self.var_interrogacao = tk.BooleanVar(value=True)
        self.check_interrogacao = tk.Checkbutton(
            frame_regras,
            text="Quebrar legenda após ponto de interrogação (?)",
            variable=self.var_interrogacao,
            font=fonte_texto, bg=bg_color, fg=fg_color,
            selectcolor="#333333", activebackground=bg_color, activeforeground="white"
        )
        self.check_interrogacao.grid(row=4, column=0, columnspan=2, sticky="w", pady=8)

        # --- SEÇÃO 3: GERAÇÃO ---
        tk.Label(root, text="", bg=bg_color).pack(pady=5)
        self.btn_gerar = tk.Button(root, text="⚡ Gerar Arquivo .SRT", font=("Segoe UI", 12, "bold"), bg="#4CAF50",
                                   fg="white", cursor="hand2", command=self.processar_legendas)
        self.btn_gerar.pack(fill="x", ipady=8)

    def selecionar_arquivo(self):
        arquivo = filedialog.askopenfilename(
            title="Selecione o JSON do WhisperX",
            filetypes=[("Arquivos JSON", "*.json")]
        )
        if arquivo:
            self.caminho_json = arquivo
            nome_arquivo = os.path.basename(arquivo)
            self.lbl_arquivo.config(text=f"✅ {nome_arquivo}", fg="#4CAF50")

    def processar_legendas(self):
        if not self.caminho_json:
            messagebox.showwarning("Atenção ⚠️", "Selecione um arquivo JSON primeiro!")
            return

        try:
            cpl = int(self.input_cpl.get())
            max_gap = float(self.input_gap.get())
            max_words = int(self.input_words.get())
            hang_time = float(self.input_hang.get())
            quebrar_interrogacao = self.var_interrogacao.get()
        except ValueError:
            messagebox.showerror("Erro 🔴", "Certifique-se de que os parâmetros numéricos são válidos.")
            return

        try:
            with open(self.caminho_json, 'r', encoding='utf-8') as f:
                dados = json.load(f)

            palavras = dados.get('word_segments', [])
            blocos_srt = []
            bloco_atual = []
            inicio_bloco = None
            fim_bloco = None

            # ETAPA 1: Agrupamento Lógico
            for p in palavras:
                if 'start' not in p or 'end' not in p:
                    continue

                palavra = p['word'].strip()
                start = p['start']
                end = p['end']

                if not bloco_atual:
                    bloco_atual.append(palavra)
                    inicio_bloco = start
                    fim_bloco = end
                    continue

                texto_simulado = " ".join(bloco_atual) + " " + palavra
                gap = start - fim_bloco

                estourou_caracteres = len(texto_simulado) > cpl
                estourou_pausa = gap > max_gap
                teve_interrogacao = quebrar_interrogacao and bloco_atual[-1].endswith('?')
                estourou_palavras = max_words > 0 and len(bloco_atual) >= max_words

                if estourou_caracteres or estourou_pausa or teve_interrogacao or estourou_palavras:
                    blocos_srt.append({'texto': " ".join(bloco_atual), 'inicio': inicio_bloco, 'fim': fim_bloco})
                    bloco_atual = [palavra]
                    inicio_bloco = start
                    fim_bloco = end
                else:
                    bloco_atual.append(palavra)
                    fim_bloco = end

            if bloco_atual:
                blocos_srt.append({'texto': " ".join(bloco_atual), 'inicio': inicio_bloco, 'fim': fim_bloco})

            # ETAPA 2: Pós-Processamento (Hang Time)
            margem_seguranca = 0.05  # 50ms para as legendas não grudarem e não dar erro de frame no Premiere

            if hang_time > 0:
                for i in range(len(blocos_srt)):
                    bloco = blocos_srt[i]

                    if i < len(blocos_srt) - 1:
                        proximo_bloco = blocos_srt[i + 1]
                        espaco_livre = proximo_bloco['inicio'] - bloco['fim']

                        # Se houver espaço livre maior que a margem, podemos esticar
                        if espaco_livre > margem_seguranca:
                            acrescimo = min(hang_time, espaco_livre - margem_seguranca)
                            bloco['fim'] += acrescimo
                    else:
                        # Se for o último bloco do vídeo, pode esticar livremente
                        bloco['fim'] += hang_time

            # ETAPA 3: Salvar o Arquivo
            caminho_srt = self.caminho_json.replace('.json', '.srt')
            with open(caminho_srt, 'w', encoding='utf-8') as f:
                for i, bloco in enumerate(blocos_srt, start=1):
                    f.write(f"{i}\n")
                    f.write(f"{segundos_para_srt(bloco['inicio'])} --> {segundos_para_srt(bloco['fim'])}\n")
                    f.write(f"{bloco['texto']}\n\n")

            messagebox.showinfo("Sucesso! 🎉", f"Legenda processada com Hang Time!\n\nSalva em:\n{caminho_srt}")

        except Exception as e:
            messagebox.showerror("Erro Fatal 💀", f"Ocorreu um erro no processamento:\n{str(e)}")


root = tk.Tk()
app = FastSubMotor(root)
root.mainloop()