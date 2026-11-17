import tkinter as tk
from tkinter import messagebox
import subprocess
import threading


def executar_fastsub():
    comando_bruto = text_whisperx.get("1.0", tk.END).strip()

    if not comando_bruto:
        messagebox.showwarning("Atenção ⚠️", "O campo do comando está vazio!")
        return

    comando_limpo = comando_bruto.replace("`\n", " ").replace("`", "")

    btn_executar.config(text="🔥 Extraindo Dados... Acompanhe abaixo", state=tk.DISABLED, bg="#ff9800")

    # Limpa o console para uma nova execução
    console_log.config(state=tk.NORMAL)
    console_log.delete("1.0", tk.END)
    console_log.insert(tk.END, "Iniciando WhisperX...\n")
    console_log.config(state=tk.DISABLED)

    def atualizar_console(texto):
        console_log.config(state=tk.NORMAL)
        console_log.insert(tk.END, texto)
        console_log.see(tk.END)  # Rola a tela para baixo automaticamente
        console_log.config(state=tk.DISABLED)

    def rodar_thread():
        try:
            # Popen com suporte explicitado a UTF-8 (evita erro de charmap no Windows)
            processo = subprocess.Popen(
                comando_limpo,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace',
                bufsize=1,
                universal_newlines=True
            )

            # Lê cada linha gerada pelo WhisperX e joga na nossa interface
            for linha in processo.stdout:
                root.after(0, atualizar_console, linha)

            processo.wait()  # Espera o processo terminar

            if processo.returncode == 0:
                root.after(0,
                           lambda: messagebox.showinfo("Sucesso! 🎉", "Extração finalizada! JSON gerado com sucesso."))
            else:
                root.after(0, lambda: messagebox.showerror("Erro 🔴", "Ocorreu uma falha. Verifique o log no console."))

        except Exception as e:
            root.after(0, lambda: messagebox.showerror("Erro Fatal 💀", f"Erro no sistema:\n{str(e)}"))
        finally:
            root.after(0, lambda: btn_executar.config(text="🚀 Iniciar FastSub", state=tk.NORMAL, bg="#4CAF50"))

    threading.Thread(target=rodar_thread, daemon=True).start()


# --- Construção da Interface Gráfica ---
root = tk.Tk()
root.title("🎬 FastSub - Motor Inteligente de Legendagem")
root.geometry("750x550")
root.configure(padx=20, pady=20)

tk.Label(root, text="Cole o comando do WhisperX:", font=("Segoe UI", 11, "bold")).pack(anchor="w")

text_whisperx = tk.Text(root, height=6, width=85, font=("Consolas", 10), bg="#1e1e1e", fg="#d4d4d4",
                        insertbackground="white")
text_whisperx.pack(pady=5)

comando_padrao = """whisperx "C:\\Users\\nedij\\Videos\\campanha marca - chicora - como que eu vou divulgar isso 2007-2044.mp4" `
  --language pt `
  --model medium `
  --align_model WAV2VEC2_ASR_LARGE_LV60K_960H `
  --device cpu `
  --compute_type float32 `
  --output_format json `
  --output_dir "C:\\Users\\nedij\\Videos\""""
text_whisperx.insert(tk.END, comando_padrao)

btn_executar = tk.Button(root, text="🚀 Iniciar FastSub", font=("Segoe UI", 12, "bold"), bg="#4CAF50", fg="white",
                         cursor="hand2", command=executar_fastsub)
btn_executar.pack(pady=10, fill="x", ipady=5)

tk.Label(root, text="Terminal (Progresso em tempo real):", font=("Segoe UI", 10, "bold")).pack(anchor="w")

# Console de Log
console_log = tk.Text(root, height=12, width=85, font=("Consolas", 9), bg="#000000", fg="#00ff00")
console_log.pack(pady=5)
console_log.config(state=tk.DISABLED)

root.mainloop()