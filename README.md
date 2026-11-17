# FastSub - Motor Inteligente de Legendagem

FastSub é um conjunto de ferramentas com interface gráfica (GUI) para geração rápida de legendas a partir de áudio/vídeo, utilizando o [WhisperX](https://github.com/m-bain/whisperX) como motor de transcrição.

O fluxo de trabalho é dividido em duas etapas:

1. **Etapa 1 (`fastsub-e1.py`)** — Extração: executa o WhisperX sobre um arquivo de vídeo/áudio e gera um JSON com a transcrição segmentada por palavras.
2. **Etapa 2 (`fastsub-e2.py`)** — Processamento: lê o JSON gerado e aplica regras de ritmo e formatação para gerar um arquivo `.srt` pronto para uso.

---

## Requisitos

### Python

- **Python 3.10** (testado com 3.10.11)
- Apenas bibliotecas da biblioteca padrão são utilizadas (`tkinter`, `subprocess`, `json`, `datetime`, `os`, `threading`).

> **Nota:** O `tkinter` já vem incluído na instalação padrão do Python no Windows. Em algumas distribuições Linux pode ser necessário instalar separadamente (ex: `sudo apt install python3-tk`).

### WhisperX

O WhisperX precisa estar instalado e acessível no terminal para que a **Etapa 1** funcione.

Siga as instruções oficiais de instalação: [https://github.com/m-bain/whisperX](https://github.com/m-bain/whisperX)

Resumo rápido:

```bash
pip install whisperx
```

> Para melhor desempenho, é recomendado ter uma GPU NVIDIA com CUDA configurado. Caso contrário, o FastSub funciona com `--device cpu` (mais lento).

---

## Como Usar

### 1. Clone o repositório

```bash
git clone https://github.com/NedisonJr/FastSub.git
cd FastSub
```

### 2. Crie um ambiente virtual (recomendado)

```bash
python -m venv .venv
```

Ative o ambiente:

- **Windows (PowerShell):**
  ```bash
  .\.venv\Scripts\Activate.ps1
  ```
- **Windows (CMD):**
  ```bash
  .\.venv\Scripts\activate.bat
  ```
- **Linux/macOS:**
  ```bash
  source .venv/bin/activate
  ```

### 3. Instale o WhisperX no ambiente virtual

```bash
pip install whisperx
```

### 4. Execute a Etapa 1 — Extração com WhisperX

```bash
python fastsub-e1.py
```

Uma janela vai abrir com um campo de texto onde você cola o comando do WhisperX. Exemplo de comando:

```
whisperx "C:\caminho\para\seu\video.mp4" --language pt --model medium --align_model WAV2VEC2_ASR_LARGE_LV60K_960H --device cpu --compute_type float32 --output_format json --output_dir "C:\caminho\para\saida"
```

Clique em **"Iniciar FastSub"** e acompanhe o progresso no terminal integrado.

### 5. Execute a Etapa 2 — Geração do .SRT

```bash
python fastsub-e2.py
```

Na janela que abrir:

1. Selecione o arquivo `.json` gerado na etapa anterior.
2. Ajuste os parâmetros de ritmo conforme necessário:
   - **CPL (Caracteres por Linha):** limite de caracteres antes de quebrar a legenda (padrão: 35).
   - **Pausa Máxima de Fôlego:** intervalo de silêncio (em segundos) que força uma nova legenda (padrão: 0.4s).
   - **Máximo de Palavras por Bloco:** limite de palavras por legenda, 0 = sem limite (padrão: 0).
   - **Hang Time:** tempo extra (em segundos) que a legenda permanece na tela após a última palavra, para facilitar a leitura (padrão: 0.3s).
   - **Quebrar após interrogação:** se ativado, força uma nova legenda após cada ponto de interrogação.
3. Clique em **"Gerar Arquivo .SRT"**.

O arquivo `.srt` será salvo no mesmo diretório do JSON.

---

## Ferramenta Complementar Recomendada

Para ajustes finos nas legendas geradas (correção de texto, sincronização manual, etc.), é altamente recomendado utilizar o **[Subtitle Edit](https://subtitleedit.org/)** — um editor de legendas gratuito e open-source para Windows.

Com o Subtitle Edit você pode:
- Visualizar e editar o `.srt` gerado pelo FastSub.
- Ajustar timings manualmente com preview de vídeo.
- Corrigir erros de transcrição.
- Converter entre formatos de legenda.

---

## Estrutura do Projeto

```
FastSub/
├── fastsub-e1.py    # Etapa 1: Interface para executar o WhisperX
├── fastsub-e2.py    # Etapa 2: Processador de JSON → SRT com regras de ritmo
└── README.md
```

---

## Licença

Este projeto é de uso livre.
